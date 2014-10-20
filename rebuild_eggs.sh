#!/bin/sh
set -e
echo "clean builds directory"
rm -r builds/* || true
mkdir -p builds/ver_a builds/ver_b

echo "Building python eggs"
cd ver_a; python setup.py bdist_egg; cd ..
cd ver_b; python setup.py bdist_egg; cd ..

echo "copying eggs into build directories"
cp ver_a/dist/fooserv-ver_a-py*.egg builds/ver_a/
cp ver_b/dist/fooserv-ver_b-py*.egg builds/ver_b/

echo "updating eggs.pth files"
find `pwd`/builds/ver_a/ -name "*.egg" > builds/ver_a/eggs.pth
find `pwd`/builds/ver_b/ -name "*.egg" > builds/ver_b/eggs.pth

