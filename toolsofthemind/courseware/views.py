"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Sep-2021

Ported from edx-platform/lms/djangoapps/courseware/views/views.py
Courseware views functions
"""

from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from common.djangoapps.util.cache import cache_if_anonymous

from common.djangoapps.edxmako.shortcuts import render_to_response
from lms.djangoapps.courseware.courses import get_courses, sort_by_start_date, sort_by_announcement
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from openedx.core.djangoapps.catalog.utils import get_programs, get_programs_with_type


@ensure_csrf_cookie
@cache_if_anonymous()
def courses(request):
    """
    Render "find courses" page.  The course selection work is done in courseware.courses.
    """
    courses_list = []
    course_discovery_meanings = getattr(settings, "COURSE_DISCOVERY_MEANINGS", {})
    if not settings.FEATURES.get("ENABLE_COURSE_DISCOVERY"):
        courses_list = get_courses(request.user)

        if configuration_helpers.get_value(
            "ENABLE_COURSE_SORTING_BY_START_DATE", settings.FEATURES["ENABLE_COURSE_SORTING_BY_START_DATE"]
        ):
            courses_list = sort_by_start_date(courses_list)
        else:
            courses_list = sort_by_announcement(courses_list)

    # Add marketable programs to the context.
    programs_list = get_programs_with_type(request.site, include_hidden=False)

    # mcdaniel sep-2021: add toolsofthemind categories here as a seperate dict.
    #
    #
    return render_to_response(
        "courseware/courses.html",
        {
            "courses": courses_list,
            "course_discovery_meanings": course_discovery_meanings,
            "programs_list": programs_list,
        },
    )
