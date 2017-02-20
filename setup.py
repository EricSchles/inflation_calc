#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

description = 'Functions and data manipulation for economics data'
with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name = 'inflation_calc',
    version = '0.1.1',
    url = 'https://github.com/EricSchles/inflation_calc',
    license = 'GPLv3',
    description = description,
    long_description = long_description,
    author = 'Eric Schles',
    author_email = 'ericschles@gmail.com',
    install_requires = [
        'datapackage',
        'argparse',
        'distribute',
        'statsmodels',
        'scipy',
        'pandas',
        'requests',
        'editdistance'
    ],
    packages = ['inflation_calc'],
    package_dir={'inflation_calc': 'inflation_calc'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Office/Business :: Financial',
        'Topic :: Utilities',
    ],
)
