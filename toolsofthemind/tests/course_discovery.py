"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Sep-2021

tests for custom menu in course discovery page.
"""
from django.contrib.auth import get_user_model
from toolsofthemind.utils import get_tom_menu_data
from lms.djangoapps.courseware.courses import get_courses


def test():

    User = get_user_model()
    me = User.objects.get(username="mcdaniel")
    courses = get_courses(me)

    retval = get_tom_menu_data(me, courses)

    return retval
