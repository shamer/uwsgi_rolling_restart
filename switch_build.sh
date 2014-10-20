#!/bin/bash
set -e
currentbuild=$(readlink build)
target=none
echo "current build is $currentbuild"
if [ "$currentbuild" = "builds/ver_b" ]
then
	target=ver_a
else
	target=ver_b
fi
echo "using $target"
ln -sfn builds/$target build

