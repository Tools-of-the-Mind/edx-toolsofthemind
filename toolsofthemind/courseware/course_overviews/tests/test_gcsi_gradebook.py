"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Sep-2021

Tests of the toolsofthemind modified course_overviews
"""
from django.urls import reverse

from capa.tests.response_xml_factory import StringResponseXMLFactory
from common.djangoapps.student.tests.factories import AdminFactory, CourseEnrollmentFactory, UserFactory
from lms.djangoapps.courseware.tests.factories import StudentModuleFactory
from lms.djangoapps.courseware.api import task_compute_all_courseware_for_course
from xmodule.modulestore.tests.django_utils import SharedModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory, ItemFactory

USER_COUNT = 11


class TestCourseSummary(SharedModuleStoreTestCase):
    """
    Test functionality of the toolsofthemind course_overviews. Sets up a course with assignments and
    students who've scored various scores on these assignments. Base class for further
    course_overviews tests.
    """

    grading_policy = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create a course with the desired grading policy (from our class attribute)
        kwargs = {}
        if cls.grading_policy is not None:
            kwargs["grading_policy"] = cls.grading_policy
        cls.course = CourseFactory.create(**kwargs)

        # Now give it some content
        with cls.store.bulk_operations(cls.course.id, emit_signals=False):
            chapter = ItemFactory.create(
                parent_location=cls.course.location,
                category="sequential",
            )
            section = ItemFactory.create(
                parent_location=chapter.location, category="sequential", metadata={"graded": True, "format": "Homework"}
            )
            cls.items = [
                ItemFactory.create(
                    parent_location=section.location,
                    category="problem",
                    data=StringResponseXMLFactory().build_xml(answer="foo"),
                    metadata={"rerandomize": "always"},
                )
                for __ in range(USER_COUNT - 1)
            ]

    def setUp(self):
        super().setUp()

        instructor = AdminFactory.create()
        self.client.login(username=instructor.username, password="test")
        self.users = [UserFactory.create() for _ in range(USER_COUNT)]

        for user in self.users:
            CourseEnrollmentFactory.create(user=user, course_id=self.course.id)

        for i, item in enumerate(self.items):
            for j, user in enumerate(self.users):
                StudentModuleFactory.create(
                    grade=1 if i < j else 0,
                    max_grade=1,
                    student=user,
                    course_id=self.course.id,
                    module_state_key=item.location,
                )
        task_compute_all_courseware_for_course.apply_async(kwargs={"course_key": str(self.course.id)})

        # mcdaniel:
        # Swapped out for our course_overviews
        self.response = self.client.get(reverse("toolsofthemind_course_overviews", args=(str(self.course.id),)))

        assert self.response.status_code == 200


class TestDefaultGradingPolicy(TestCourseSummary):
    """
    Tests that the grading policy is properly applied for all users in the course
    Uses the default policy (50% passing rate)
    """

    def test_all_users_listed(self):
        for user in self.users:
            assert user.username in str(self.response.content, "utf-8")

    def test_default_policy(self):
        # Default >= 50% passes, so Users 5-10 should be passing for Homework 1 [6]
        # One use at the top of the page [1]
        assert 7 == self.response.content.count(b"grade_Pass")

        # Users 1-5 attempted Homework 1 (and get Fs) [4]
        # Users 1-10 attempted any homework (and get Fs) [10]
        # Users 4-10 scored enough to not get rounded to 0 for the class (and get Fs) [7]
        # One use at top of the page [1]
        assert 23 == self.response.content.count(b"grade_F")

        # All other courseware are None [29 categories * 11 users - 27 non-empty courseware = 292]
        # One use at the top of the page [1]
        assert 292 == self.response.content.count(b"grade_None")


class TestLetterCutoffPolicy(TestCourseSummary):
    """
    Tests advanced grading policy (with letter grade cutoffs). Includes tests of
    UX display (color, etc).
    """

    grading_policy = {
        "GRADER": [
            {"type": "Homework", "min_count": 1, "drop_count": 0, "short_label": "HW", "weight": 1},
        ],
        "GRADE_CUTOFFS": {
            "A": 0.9,
            "B": 0.8,
            "C": 0.7,
            "D": 0.6,
        },
    }

    def test_styles(self):

        self.assertContains(self.response, "grade_A {color:green;}")
        self.assertContains(self.response, "grade_B {color:Chocolate;}")
        self.assertContains(self.response, "grade_C {color:DarkSlateGray;}")
        self.assertContains(self.response, "grade_D {color:DarkSlateGray;}")

    def test_assigned_courseware(self):
        # Users 9-10 have >= 90% on Homeworks [2]
        # Users 9-10 have >= 90% on the class [2]
        # One use at the top of the page [1]
        assert 5 == self.response.content.count(b"grade_A")

        # User 8 has 80 <= Homeworks < 90 [1]
        # User 8 has 80 <= class < 90 [1]
        # One use at the top of the page [1]
        assert 3 == self.response.content.count(b"grade_B")

        # User 7 has 70 <= Homeworks < 80 [1]
        # User 7 has 70 <= class < 80 [1]
        # One use at the top of the page [1]
        assert 3 == self.response.content.count(b"grade_C")

        # User 6 has 60 <= Homeworks < 70 [1]
        # User 6 has 60 <= class < 70 [1]
        # One use at the top of the page [1]
        assert 3 == self.response.content.count(b"grade_C")

        # Users 1-5 have 60% > courseware > 0 on Homeworks [5]
        # Users 1-5 have 60% > courseware > 0 on the class [5]
        # One use at top of the page [1]
        assert 11 == self.response.content.count(b"grade_F")

        # User 0 has 0 on Homeworks [1]
        # User 0 has 0 on the class [1]
        # One use at the top of the page [1]
        assert 3 == self.response.content.count(b"grade_None")
