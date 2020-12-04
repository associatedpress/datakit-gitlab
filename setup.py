#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DataKit GitLab plugin
---------------------

`datakit-gitlab` is a plugin for `datakit <https://datakit.ap.org/>`_ to
streamline the process of integrating your project with a GitLab repository.

For more information, see `the project's home page <https://github.com/associatedpress/datakit-gitlab>`_.
"""

from setuptools import setup, find_packages

requirements = [
    'cliff',
    'datakit-core',
    'python-gitlab>=2.5.0'
]

test_requirements = [
    'pytest',
    'pytest-catchlog',
    'pytest-mock==1.5.0',
    'responses==0.5.1'
]

setup(
    name='datakit-gitlab',
    version='0.4.0',
    description="Commands to manage project integration with Gitlab.",
    long_description=__doc__,
    author="Serdar Tumgoren",
    author_email='stumgoren@ap.org',
    url='https://github.com/associatedpress/datakit-gitlab',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'datakit.plugins': [
            'gitlab integrate=datakit_gitlab:Integrate',
            'gitlab issues add=datakit_gitlab:issues.Add',
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
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
