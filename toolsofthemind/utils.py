"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Sep-2021

toolsofthemind utils.
"""

# Python
import logging

# Django
from django.db.models import Subquery

# Open edX
from lms.djangoapps.courseware.exceptions import CourseRunNotFound
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview

# This repo
from toolsofthemind.models import (
    TOMCourseGroups,
    TOMStudentCourseGroups,
    TOMCourseSubgroups,
    TOMCourseMenu,
)

log = logging.getLogger(__name__)


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
                "id": course_group.id,
                "course_group": course_group.course_group,
                "subgroups": _get_subgroups_for_group(course_group, courses),
            }
        )

    log.info("DEBUG: retval={retval}".format(retval=retval))
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

        # get_course() returns a CourseRunNotFound exception
        # if for example, the course run has not yet been published.
        # there are a variety of other reasons why this exception could
        # be raiseed.
        #
        # importantly, if this particular exception is raised
        # then we should not include the course in the menu.
        try:
            course = CourseOverview.get_from_id(course_locator)
        except CourseRunNotFound:
            log.error(
                "CourseRunNotFound exception encountered for {data_type} {course_locator}".format(
                    course_locator=course_locator, data_type=type(course_locator)
                )
            )
            course = None

        if course and course in list(courses):
            retval.append(course)

    return retval
