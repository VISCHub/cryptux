[![Build Status](https://travis-ci.org/VISCHub/crypto-wallets.svg?branch=master)](https://travis-ci.org/VISCHub/crypto-wallets)

# crypto-wallets
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

A sample session would go like this:

```
$ ./cryptux -t BITCOIN
Private key format (WIF/HEX/NEW):
    new
Network type (MAINNET/TESTNET): mainnet
Public key format (COMPRESSED/UNCOMPRESSED): compressed
================================================================
Remember to protect the Private Key!
================================
Private Key in HEX: 460A10378746800A048E131075B09286A219527DAB2EE9EEEB34C4CD44F31469
Private Key in WIF: KyZrj4XaKTNmS6XCxGRgicCN3FVXkPnzeJgfmKEUEBVJMsrBazdi
================================================================
Network type:
    MAINNET
Public key format:
    COMPRESSED
Generated Bitcoin address:
    1P3vwh8kyhWszcqvAaBS6JBP5dxNXdef8R
================================================================
```
