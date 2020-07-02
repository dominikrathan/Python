#!/usr/bin/env python3
# pylint: disable=missing-docstring

from setuptools import setup

with open('README.md', 'r') as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name='my_owm',
    version='1.0',
    description='open weather map command line client',
    long_description=LONG_DESCRIPTION,
    author=['Lukáš Macek', 'Dominik Rathan'],
    author_email=['luk1998@seznam.cz', 'rathan.dominik@gmail.com'],
    packages=['owm', 'user', 'zebra'],
    install_requires=['requests'],
    scripts=['./my_owm'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'my_owm=zebra.my_owm:main'
        ]
    }
)
