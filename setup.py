#!/usr/bin/env python

# Read https://github.com/django-extensions/django-extensions/issues/92
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='CryptoWallets',
      version='0.0.1',
      description='Sample wallets for Cryptocurrencies',
      author='Viet Le',
      author_email='vietlq85@gmail.com',
      url='https://github.com/VISCHub/crypto-wallets',
      packages=['bitcoin'])
