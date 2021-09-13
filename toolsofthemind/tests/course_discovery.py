"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Sep-2021

tests for custom menu in course discovery page.
"""
from django.contrib.auth import get_user_model
from django.db.models import Subquery

from toolsofthemind.utils import get_tom_menu_data
from lms.djangoapps.courseware.courses import get_courses

from toolsofthemind.models import (
    TOMCourseGroups,
    TOMStudentCourseGroups,
    TOMCourseSubgroups,
    TOMCourseMenu,
)


def test():

    User = get_user_model()
    me = User.objects.get(username="mcdaniel")
    courses = get_courses(me)

    retval = get_tom_menu_data(me, courses)

    return retval
