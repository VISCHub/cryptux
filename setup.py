#!/usr/bin/env python

# Read https://github.com/django-extensions/django-extensions/issues/92
# Read: http://setuptools.readthedocs.io/en/latest/setuptools.html
# Look for find_packages, packages, package_dir
from setuptools import setup, find_packages
import codecs

import cryptux

with codecs.open('README.rst', 'r', 'utf-8') as fd:
    long_description = fd.read()

setup(
    name='cryptux',
    version=cryptux.__version__,
    description='Simple wallet for Cryptocurrencies',
    long_description=long_description,
    author='Viet Le',
    author_email='vietlq85@gmail.com',
    url='https://github.com/VISCHub/cryptux',
    install_requires=['ecdsa>=0.13'],
    packages=find_packages(),
    scripts=['tools/cryptux'],
    keywords=['crypto hdw wallet bitcoin ether'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ])
