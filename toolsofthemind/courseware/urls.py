"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Sep-2021

Tools of the Mind Courseware Module URLs.
"""
# Django
from django.conf.urls import include, url

# this repo
from toolsofthemind.courseware.course_overviews import urls as course_overviews_urls

app_name = "toolsofthemind.courseware"

urlpatterns = [
    url(
        r"^course_overviews/",
        include(
            (course_overviews_urls.urlpatterns, "toolsofthemind.courseware"),
            namespace="toolsofthemind_courseware_course_overviews",
        ),
    ),
]
