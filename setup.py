import os
from setuptools import find_packages, setup
from toolsofthemind.version import __version__

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="edx-toolsofthemind",
    version=__version__,
    packages=find_packages(),
    package_data={"": ["*.html"]},  # include any Mako templates found in this repo.
    include_package_data=True,
    license="Proprietary",
    description="Adds custom Open edX functionality",
    long_description="",
    author="Lawrence McDaniel",
    author_email="lpm0073@gmail.com",
    url="https://github.com/Tools-of-the-Mind/edx-toolsofthemind",
    install_requires=[
        # mcdaniel Sep-2021
        #
        # don't add packages that are already required by open-edx.
        # this only increases the risk version conflicts in production.
    ],
    zip_safe=False,
    keywords="Django edx",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        # mcdaniel Sep-2021
        #
        # IMPORTANT: ensure that this entry_points coincides with that of edx-platform
        #            and also that you are not introducing any name collisions.
        # https://github.com/edx/edx-platform/blob/main/setup.py#L88
        "lms.djangoapp": [
            "toolsofthemind = toolsofthemind.apps:TOMConfig",
        ],
    },
    extras_require={
        "Django": ["Django>=2.2,<2.3"],
    },
)
