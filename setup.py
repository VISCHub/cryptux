#!/usr/bin/env python

# Read https://github.com/django-extensions/django-extensions/issues/92
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Read: http://setuptools.readthedocs.io/en/latest/setuptools.html
# Look for find_packages, packages, package_dir

setup(name='cryptux',
      version='0.0.2',
      description='Simple wallet for Cryptocurrencies',
      author='Viet Le',
      author_email='vietlq85@gmail.com',
      url='https://github.com/VISCHub/cryptux',
      install_requires=['ecdsa>=0.13'],
      packages=['src/cryptux'],
      scripts=['tools/cryptux'],
      keywords=['crypto', 'hdw', 'wallet', 'bitcoin', 'ether'],
      classifiers=[])
