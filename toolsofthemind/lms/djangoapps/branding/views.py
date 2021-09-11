"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Sep-2021

Ported from edx-platform/lms/djangoapps/branding/views.py
Views for the branding app.
"""
# django
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import redirect
from django.http import Http404

# open edx
from common.djangoapps.util.cache import cache_if_anonymous
from common.djangoapps.edxmako.shortcuts import marketing_link
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers

# toolsofthemind
import toolsofthemind.lms.djangoapps.courseware.views as toolsofthemind_courseware_views


@ensure_csrf_cookie
@cache_if_anonymous()
def courses(request):
    """
    Render the "find courses" page. If the marketing site is enabled, redirect
    to that. Otherwise, if subdomain branding is on, this is the university
    profile page. Otherwise, it's the edX courseware.views.views.courses page
    """
    enable_mktg_site = configuration_helpers.get_value(
        "ENABLE_MKTG_SITE", settings.FEATURES.get("ENABLE_MKTG_SITE", False)
    )

    if enable_mktg_site:
        return redirect(marketing_link("COURSES"), permanent=True)

    # if not settings.FEATURES.get("COURSES_ARE_BROWSABLE"):
    #    raise Http404

    # mcdaniel sep-2021: we're only porting this def so that we can substitute
    # our modified courseware_views.courses() here.
    return toolsofthemind_courseware_views.courses(request)
