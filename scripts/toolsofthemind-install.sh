#!/bin/bash
#---------------------------------------------------------
# written by: lawrence mcdaniel
#             https://lawrencemcdaniel.com
#
# usage:     update a local clone of a private git repo.
#            $INSTALL_ROOT is supposed to be equal to the relative
#            path in which Tutor searches for "local" requirements
#---------------------------------------------------------

REPO_NAME="edx-toolsofthemind"
BRANCH="main"
INSTALL_ROOT="~/"
INSTALL_PATH=$INSTALL_ROOT/$REPO_NAME

echo "cloning Github repository "$REPO_NAME
if [ -d $INSTALL_PATH ]; then
    sudo rm -r $INSTALL_PATH
fi
git clone -b $BRANCH git@github-toolsofthemind:TransformCore/$REPO_NAME.git $INSTALL_PATH
echo "done."
echo "copying local installation scripts"
cp $INSTALL_PATH/tutor-installer/*.* ~/
chmod 755 ~/*.sh
echo "done."
