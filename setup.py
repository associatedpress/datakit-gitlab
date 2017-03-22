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
]

test_requirements = [
    'pytest'
]

setup(
    name='datakit-gitlab',
    version='0.1.0',
    description="Commands to manage project integration with Gitlab.",
    long_description=readme + '\n\n' + history,
    author="Serdar Tumgoren",
    author_email='stumgoren@ap.org',
    url='https://github.com/zstumgoren/datakit-gitlab',
    packages=[
        'datakit_gitlab',
    ],
    package_dir={'datakit_gitlab':
                 'datakit_gitlab'},
    include_package_data=True,
    entry_points={
        'datakit.plugins': [
            #'fancyplugin:greet= datakit_gitlab.greet:Greet',
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
