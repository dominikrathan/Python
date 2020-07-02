#!/usr/bin/env python3
# pylint: disable=missing-docstring

from setuptools import setup

with open('README', 'r') as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name='my_ssg',
    version='1.0',
    description='static site generator',
    long_description=LONG_DESCRIPTION,
    author='Dominik Rathan',
    author_email='rathan.dominik@gmail.com',
    packages=['matfyz.nswi177'],
    install_requires=['jinja2', 'pytidylib', 'markdown', 'pyyaml'],
    scripts=['./my_ssg'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'my_ssg=matfyz.nswi177.my_ssg:main'
        ]
    }
)
