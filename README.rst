.. image:: https://badge.fury.io/py/cryptux.svg
    :target: https://badge.fury.io/py/cryptux
.. image:: https://travis-ci.org/VISCHub/cryptux.svg?branch=master
    :target: https://travis-ci.org/VISCHub/cryptux

================================================================
cryptux
================================================================

A simple wallet for cryptocurrencies that can:

* Create, import, export accounts
* Sign transactions

================================================================
Usage
================================================================

The interactive tool ``cryptux`` is meant to be simple:

.. code-block::

    $ cryptux
    usage: cryptux [-h] [-t {BITCOIN}]

    optional arguments:
      -h, --help            show this help message and exit
      -t {BITCOIN}, --coin-type {BITCOIN}
                            coin type to generate account address for

At the moment of writing, only Bitcoin is supported. Ethereum account support is coming soon.

================================================================
Developer Guide
================================================================

Before trying to run ``tools/cryptux`` locally, make sure it uses local libraries by running:

.. code-block:: bash

    python setup.py develop

It's highly recommended that you use the package ``virtualenvwrapper``.

To test the changes without publishing to PyPI, force pip to install from local dir:

.. code-block:: bash

    pip install -e /path/to/cryptux

Publishing to test PyPI can be done via this command:

.. code-block:: bash

    python setup.py sdist upload -r testpypi

Use ``flake8`` to detect ``PEP8`` violations and format code nicely using ``yapf -i``, do check the project `YAPF <https://github.com/google/yapf>`_.

================================================================
Bitcoin
================================================================

There are 3 ways to generate a Bitcoin address with ``cryptux``:

* Generate from private key in HEX
* Generate from private key in WIF format
* Generate private key offline and derive account address

A sample session would go like this:

.. code-block::

    $ cryptux -t BITCOIN
    Private key format (WIF/HEX/NEW): new
    Network type (MAINNET/TESTNET): mainnet
    Public key format (COMPRESSED/UNCOMPRESSED): compressed
    ================================================================
    Remember to protect the Private Key!
    ================================
    Private Key in HEX: 7161B2F99B4F0DB740C27A35B55FDDAE0FD90A8C23789291106667D29F1859F6
    Private Key in WIF: L127LBiTmhFXoXsz1qymwNrbsmk1s71kBycoi5VH3i22tDekzYY1
    ================================================================
    Network type: MAINNET
    Public key format: COMPRESSED
    Generated Bitcoin address: 193GxFgNCtpvsYPnWErEvXNETgGiJ7HG5F
    ================================================================
