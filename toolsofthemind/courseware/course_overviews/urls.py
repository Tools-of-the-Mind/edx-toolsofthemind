"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Sep-2021

CourseSummary URLs.
"""

from django.conf import settings
from django.conf.urls import url

# from toolsofthemind.courseware.course_overviews.views.some_custom_view import some_view_def

app_name = "toolsofthemind.courseware"

urlpatterns = [
    # provide routing support with and without pagination
    # url(fr"^courses/{settings.COURSE_ID_PATTERN}/$", some_view_def, name="some_view_def"),
    # url(fr"^courses/{settings.COURSE_ID_PATTERN}/(?P<offset>[0-9]+)$", some_view_def, name="some_view_def"),
]
