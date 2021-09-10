#!/bin/bash
#---------------------------------------------------------
# written by: lawrence mcdaniel
#             https://lawrencemcdaniel.com
#
# usage:     update a local clone of a private git repo.
#            $INSTALL_ROOT is supposed to be equal to the relative
#            path in which Tutor searches for "local" requirements
#---------------------------------------------------------

sudo -H -u edxapp bash << EOF
source /edx/app/edxapp/edxapp_env
source /edx/app/edxapp/venvs/edxapp/bin/activate
pip install git+https://github.com/Tools-of-the-Mind/edx-toolsofthemind.git
EOF
