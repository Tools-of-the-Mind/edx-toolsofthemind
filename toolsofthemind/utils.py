"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Sep-2021

toolsofthemind utils.
"""

# Django
from django.views.decorators.csrf import ensure_csrf_cookie

# This repo
from toolsofthemind.models import (
    TOMStudentCourseGroups,
    TOMCourseSubgroups,
    TOMCourseGroups,
    TOMCourseMenu,
)


@ensure_csrf_cookie
def get_menu_categories(request):
    """
    Return a Django ORM dictionary of the Tools of the Mind courses that are available
    to this user.
    """
    course_groups_list = TOMStudentCourseGroups.objects.filter(user=request.user)
    course_subgroups_list = TOMCourseSubgroups.objects.filter(course_groups__in=course_groups_list)
    course_menu = TOMCourseMenu.objects.filter(course_subgroup__in=course_subgroups_list)

    return course_menu
