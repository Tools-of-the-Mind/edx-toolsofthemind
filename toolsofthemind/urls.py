"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Sep-2021

Tools of the Mind custom URLs - courseware
"""
# Django
from django.conf.urls import url, include

# This repo
from toolsofthemind.courseware import urls as courseware_urls

app_name = "toolsofthemind"

urlpatterns = [
    url(r"^courseware/", include((courseware_urls.urlpatterns, "toolsofthemind.courseware"), namespace="toolsofthemind_courseware")),
]
