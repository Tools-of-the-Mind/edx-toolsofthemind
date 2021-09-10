"""
Common Pluggable Django App settings
"""
from path import Path as path

PACKAGE_ROOT = path(__file__).abspath().dirname().dirname()  # /toolsofthemind
REPO_ROOT = PACKAGE_ROOT.dirname()  # toolsofthemind-digital-learning-openedx
TEMPLATES_DIR = PACKAGE_ROOT / "templates"


def plugin_settings(settings):
    """
    Injects additional Django settings into lms.envs.common
    """
    # Add the template directory for this package to
    # to the search path for Mako.
    settings.MAKO_TEMPLATE_DIRS_BASE.extend([TEMPLATES_DIR])
