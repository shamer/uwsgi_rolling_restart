#!/usr/bin/python
from setuptools import setup, find_packages
import time

version = 'ver_a'
name = 'fooserv'
packages = ['%s.%s' % (name, p) for p in find_packages(name)]
packages.append(name)
setup(version=version, name=name, packages=packages)

