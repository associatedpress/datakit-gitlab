#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'cliff',
    'datakit-core',
    'python-gitlab==0.19'
]

test_requirements = [
    'pytest',
    'pytest-catchlog',
    'pytest-mock==1.5.0',
    'responses==0.5.1'
]

setup(
    name='datakit-gitlab',
    version='0.1.0',
    description="Commands to manage project integration with Gitlab.",
    long_description=readme + '\n\n' + history,
    author="Serdar Tumgoren",
    author_email='stumgoren@ap.org',
    url='https://gitlab.inside.ap.org:newsapps/datakit-gitlab',
    packages=[
        'datakit_gitlab',
    ],
    package_dir={'datakit_gitlab':
                 'datakit_gitlab'},
    include_package_data=True,
    entry_points={
        'datakit.plugins': [
            'gitlab:integrate= datakit_gitlab:Integrate',
            'gitlab:issues:add= datakit_gitlab:issues.Add',
        ]
    },
    install_requires=requirements,
    license="ISC license",
    zip_safe=False,
    keywords='datakit-gitlab',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
