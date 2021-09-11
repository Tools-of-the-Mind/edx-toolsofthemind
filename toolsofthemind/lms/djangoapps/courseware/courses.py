"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Sep-2021

Ported from edx-platform/lms/djangoapps/courseware/courses.py
Functions for accessing and displaying courses within the
courseware.
"""

# django
from django.conf import settings

# open edx
from edx_django_utils.monitoring import function_trace
from lms.djangoapps import branding
from lms.djangoapps.courseware.access import has_access
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from openedx.core.lib.api.view_utils import LazySequence


@function_trace("get_courses")
def get_courses(user, org=None, filter_=None):
    """
    Return a LazySequence of courses available, optionally filtered by org code (case-insensitive).
    """
    courses = (
        branding.get_visible_courses(
            org=org,
            filter_=filter_,
        )
        .prefetch_related(
            "modes",
        )
        .select_related("image_set")
    )

    permission_name = configuration_helpers.get_value(
        "COURSE_CATALOG_VISIBILITY_PERMISSION", settings.COURSE_CATALOG_VISIBILITY_PERMISSION
    )

    return LazySequence((c for c in courses if has_access(user, permission_name, c)), est_len=courses.count())
