# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
import sys
__VERSION__ = '0.1'

assert sys.version_info[0] == 3, "gorra requires Python > 3"

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()


setup(
    name="gorra",
    version='0.1',
    py_modules=['gorra'],
    install_requires=[
        'click',
        'pyyaml',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        gorra=gorra.cli:main
    ''',
)
