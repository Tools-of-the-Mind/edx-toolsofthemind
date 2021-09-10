"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Sep-2021

Courseware App Configuration
"""
import logging

from django.apps import AppConfig

log = logging.getLogger(__name__)


class CoursewareConfig(AppConfig):
    name = "toolsofthemind.courseware"
    label = "toolsofthemind.courseware"
    verbose_name = "Tools of the Mind Courseware Module Enhancements"

    def ready(self):
        from . import signals  # pylint: disable=unused-import, import-outside-toplevel

        log.debug("{label} is ready.".format(label=self.label))
