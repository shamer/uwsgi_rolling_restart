#!/bin/sh
set -e
echo "clean builds directory"
rm -r builds/*
mkdir builds/ver_a builds/ver_b

echo "Building python eggs"
cd ver_a; python setup.py bdist_egg; cd ..
cd ver_b; python setup.py bdist_egg; cd ..

echo "copying eggs into build directories"
cp ver_a/dist/fooserv-ver_a-py*.egg builds/ver_a/
cp ver_b/dist/fooserv-ver_b-py*.egg builds/ver_b/

echo "updating eggs.pth files"
ls builds/ver_a/fooserv-ver_a-py*.egg > builds/ver_a/eggs.pth
ls builds/ver_b/fooserv-ver_b-py*.egg > builds/ver_b/eggs.pth

