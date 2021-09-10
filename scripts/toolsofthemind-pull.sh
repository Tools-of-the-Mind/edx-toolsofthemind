#!/bin/bash
#---------------------------------------------------------
# written by: lawrence mcdaniel
#             https://lawrencemcdaniel.com
#
# usage:     update an already-installed repo.
#            pulls from the current branch.
#---------------------------------------------------------

REPO_NAME="edx-toolsofthemind"
BRANCH="main"
INSTALL_ROOT="~/"
INSTALL_PATH=$INSTALL_ROOT/$REPO_NAME


cd $INSTALL_PATH
pwd
echo "pulling recent commits from $REPO_NAME"
git checkout $BRANCH
git pull
cd ~/edx.scripts
./edx.platform-restart.sh
