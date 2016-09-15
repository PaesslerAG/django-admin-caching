#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import django_admin_caching

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = django_admin_caching.__version__

if sys.argv[-1] == 'publish':
    os.system('make release')
    sys.exit()

readme = open('README.rst').read()

description = "Django Admin caching made easy"

setup(
    name='django_admin_caching',
    version=version,
    description=description,
    long_description=readme,
    author='Paessler AG',
    author_email='bis@paessler.com',
    url='https://github.com/PaesslerAG/django-admin-caching',
    packages=[
        'django_admin_caching',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.8',
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-admin-caching',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)