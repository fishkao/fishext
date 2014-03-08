#!/usr/bin/env python
from setuptools import setup


PACKAGE = "fishext"
VERSION = "1.0"

setup(
    name=PACKAGE,
    version=VERSION,
    description="get all the customized data such as comment, bug, bug details, bug distribution",
    author="yilan",
    packages=["fishext"],
    entry_points={
        'reviewboard.extensions':
            '%s = fishext.extension:FishExtension'
            % PACKAGE,
    },
    package_data={
        'fishext': [
            'templates/fishext/*.html',
        ],
    }
)