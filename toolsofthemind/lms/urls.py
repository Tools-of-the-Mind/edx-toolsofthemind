"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Sep-2021

Tools of the Mind custom URLs - courseware
https://learn.toolsofthemind.org/toolsofthemind/{URL PATTERNS START HERE...}
"""
# Django
from django.conf.urls import url, include

# This repo
from toolsofthemind.lms.djangoapps.branding import views as branding_views

app_name = "toolsofthemind"

urlpatterns = [
    url(r"^courses/?$", branding_views.courses, name="courses"),
]
