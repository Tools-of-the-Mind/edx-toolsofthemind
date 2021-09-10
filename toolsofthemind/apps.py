"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Sep-2021

toolsofthemind App Configuration

See: Create a new Django app in its own Git repository
     https://openedx.atlassian.net/wiki/spaces/AC/pages/28967836/Feature+Plugins+for+edX+Platform

"""
import logging

from django.apps import AppConfig

log = logging.getLogger(__name__)


class TOMConfig(AppConfig):
    name = "toolsofthemind"
    label = "toolsofthemind"
    verbose_name = "Tools of the Mind"

    # See: https://edx.readthedocs.io/projects/edx-django-utils/en/latest/edx_django_utils.plugins.html
    plugin_app = {
        # mcdaniel Sep-2021
        # this is how you inject a python list of urls into lms.urls.py
        #
        # The three dict attributes literally equate to the following
        # lines of code being injected into edx-platform/lms/urls.py:
        #
        # import toolsofthemind.urls.py
        # url(r"^toolsofthemind/", include((urls, "toolsofthemind"), namespace="toolsofthemind")),
        "url_config": {
            "lms.djangoapp": {
                "namespace": "toolsofthemind",
                "regex": "^toolsofthemind/",
                "relative_path": "urls",
            },
        },
        # mcdaniel Sep-2021
        # this is how you inject settings into lms.envs.common.py and lms.envs.production.py
        # relative_path == a python module in this repo
        #
        # This dict causes all constants defined in this settings/common.py and settings.production.py
        # to be injected into edx-platform/lms/envs/common.py and edx-platform/lms/envs/production.py
        # Refer to settings/common.py and settings.production.py for example implementation patterns.
        "settings_config": {
            "lms.djangoapp": {
                "common": {"relative_path": "settings.common"},
                "production": {"relative_path": "settings.production"},
            },
        },
    }

    def ready(self):
        log.debug("{label} is ready.".format(label=self.label))
