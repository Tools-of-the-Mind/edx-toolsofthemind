"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Sep-2021

toolsofthemind utils.
"""

# Django
from django.db.models import Subquery

# Open edX
from lms.djangoapps.courseware.courses import get_course

# This repo
from toolsofthemind.models import (
    TOMCourseGroups,
    TOMStudentCourseGroups,
    TOMCourseSubgroups,
    TOMCourseMenu,
)


def get_tom_menu_data(user, courses):
    """
    Return a Django ORM dictionary of the Tools of the Mind courses that are available
    to this user.

    inputs:
    -------
    user: Open edX Django user object

    courses: list of CourseOverview objects reeturned by lms.djangoapps.courseware.courses.get_courses()
             the list of courses deemed available to the user based on whatever policies
             are presently in place to grant/restrict access to each course run.

    see: openedx.core.djangoapps.courses.models.CourseOverview
    """
    student_course_groups = TOMStudentCourseGroups.objects.filter(user=user)
    course_groups = TOMCourseGroups.objects.filter(
        course_group__in=Subquery(student_course_groups.values("course_group"))
    )

    retval = []

    for course_group in course_groups:
        retval.append(
            {
                "course_group": course_group.course_group,
                "subgroups": _get_subgroups_for_group(course_group, courses),
            }
        )

    return retval


def _get_subgroups_for_group(course_group, courses):
    """
    Returns the subgroup list for this course_group, each enhanced with
    its respective courses list.
    """
    subgroups = TOMCourseSubgroups.objects.filter(course_group=course_group).order_by("ordinal_position")
    retval = []

    for subgroup in subgroups:
        retval.append(
            {
                "id": subgroup.id,
                "ordinal_position": subgroup.ordinal_position,
                "course_subgroup": subgroup.course_subgroup,
                "courses": _get_courses_for_subgroup(subgroup, courses),
            }
        )

    return retval


def _get_courses_for_subgroup(subgroup, courses):
    """
    Returns the cross of the contents of the subgroup's
    course list and the courses list input parameter

    inputs:
    ------
    subgroup: a Django ORM TOMCourseSubgroups object

    courses: the courses which this user can see.
    """
    courses_in_menu = TOMCourseMenu.objects.filter(course_subgroup=subgroup).values("course")
    retval = []

    for course_menu_item in courses_in_menu:
        course_locator = course_menu_item["course"]
        course = get_course(course_locator)
        if course in list(courses):
            retval.append(course)

    return retval


def test():
    """
    from django.db.models import Subquery
    from django.contrib.auth import get_user_model
    from toolsofthemind.utils import get_tom_menu_data
    from lms.djangoapps.courseware.courses import get_courses
    from toolsofthemind.models import (
        TOMCourseGroups,
        TOMStudentCourseGroups,
        TOMCourseSubgroups,
        TOMCourseMenu,
    )

    User = get_user_model()
    me = User.objects.get(username="mcdaniel")
    courses = get_courses(me)

    retval = get_tom_menu_data(me, courses)

            course_groups = TOMCourseGroups.objects.all()

                # get a list of the course groups assigned to this user.
                course_groups_list = TOMStudentCourseGroups.objects.filter(user=user)

                # get a list of all course sub-groups related to the user's course groups
                course_subgroups_list = TOMCourseSubgroups.objects.filter(
                    course_group__in=Subquery(course_groups_list.values("course_group"))
                )

                # get a list of all courses related to the course sub-groups
                course_menu = TOMCourseMenu.objects.filter(course_subgroup__in=Subquery(course_subgroups_list.values("id")))
                course_menu = list(course_menu.values("id", "course_subgroup_id", "course_id"))
    """
