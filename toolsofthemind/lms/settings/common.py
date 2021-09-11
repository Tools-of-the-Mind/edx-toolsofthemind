"""
Common Pluggable Django App settings
"""
from path import Path as path

PACKAGE_ROOT = path(__file__).abspath().dirname().dirname()  # /toolsofthemind
REPO_ROOT = PACKAGE_ROOT.dirname()  # edx-toolsofthemind
LMS_TEMPLATES_DIR = PACKAGE_ROOT / "lms" / "templates"


def plugin_settings(settings):
    """
    Injects additional Django settings into lms.envs.common
    """
    # Add the template directories for this package to
    # to the search path for Mako.
    settings.MAKO_TEMPLATE_DIRS_BASE.extend([LMS_TEMPLATES_DIR])
