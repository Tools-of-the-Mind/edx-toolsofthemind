"""
Common Pluggable Django App settings
"""


def plugin_settings(settings):
    """
    Injects additional Django settings into lms.envs.production
    """

    # mcdaniel Sep-2021
    # sample settings. safe to delete.
    env_tokens = getattr(settings, "toolsofthemind_SOME_IMPORTANT_ENV_VARIABLE", {})
    if env_tokens.get("BLAH_BLAH"):
        settings.toolsofthemind_PARAM_STUFF["blah"] = env_tokens["BLAH_BLAH"]
