"""
Common Pluggable Django App settings
"""
from path import Path as path

LMS_ROOT = path(__file__).abspath().dirname().dirname()  # /toolsofthemind/lms
LMS_TEMPLATES_DIR = LMS_ROOT / "templates"


def plugin_settings(settings):
    """
    Injects additional Django settings into lms.envs.common
    """
    # Add the template directories for this package to
    # to the search path for Mako.
    settings.MAKO_TEMPLATE_DIRS_BASE.extend([LMS_TEMPLATES_DIR])
