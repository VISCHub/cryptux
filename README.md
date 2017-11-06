[![Build Status](https://travis-ci.org/VISCHub/cryptux.svg?branch=master)](https://travis-ci.org/VISCHub/cryptux)

# cryptux
Wallet for cryptocurrencies created with education purposes. You can use cryptux to operate on cryptocurrency wallets. You can interactivele generate accounts addresses to receive cryptocurrencies.

## Usage

The interactive tool `cryptux` is meant to be simple:

```
$ cryptux
usage: cryptux [-h] [-t {BITCOIN}]

optional arguments:
  -h, --help            show this help message and exit
  -t {BITCOIN}, --coin-type {BITCOIN}
                        coin type to generate account address for
```

At the moment of writing, only Bitcoin is supported. Ethereum account support is coming soon.

## Bitcoin

To generate a Bitcoin address one is given 3 choices:
+ Generate from private key in HEX
+ Generate from private key in WIF format
+ Generate private key offline and derive account address

A sample session would go like this:

```
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
```
