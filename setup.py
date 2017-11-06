#!/usr/bin/env python

# Read https://github.com/django-extensions/django-extensions/issues/92
# Read: http://setuptools.readthedocs.io/en/latest/setuptools.html
# Look for find_packages, packages, package_dir
from setuptools import setup, find_packages

setup(name='cryptux',
      version='0.0.4',
      description='Simple wallet for Cryptocurrencies',
      author='Viet Le',
      author_email='vietlq85@gmail.com',
      url='https://github.com/VISCHub/cryptux',
      install_requires=['ecdsa>=0.13'],
      packages=find_packages('src'),  # include all packages under src
      package_dir={'': 'src'},   # tell distutils packages are under src
      scripts=['tools/cryptux'],
      keywords=['crypto hdw wallet bitcoin ether'],
      classifiers=[])
