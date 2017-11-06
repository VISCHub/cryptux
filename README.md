[![Build Status](https://travis-ci.org/VISCHub/crypto-wallets.svg?branch=master)](https://travis-ci.org/VISCHub/crypto-wallets)

# accounts-wallets
Code examples for operating on Cryptocurrency accounts and wallets. The library also provides an interactive tool `cryptux` to generate accounts addresses to receive cryptocurrencies.

## Usage

The interactive tool `cryptux` is meant to be simple:

```
$ ./cryptux
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
