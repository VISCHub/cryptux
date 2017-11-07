from .base58 import Base58
from cryptux.bitcoin.constants import MAINNET, TESTNET
from cryptux.bitcoin.constants import COMPRESSED, UNCOMPRESSED
from cryptux.bitcoin.constants import NETWORK_TYPES, PRIVKEY


def priv_key_to_wif(priv_key_raw, network_type, key_fmt):
    '''Serialise Private Key to WIF'''
    if network_type not in [MAINNET, TESTNET]:
        raise Exception('Unsupported network type: %s' % network_type)
    prefix = NETWORK_TYPES[network_type][PRIVKEY]
    if key_fmt == COMPRESSED:
        payload = priv_key_raw + b'\x01'
    elif key_fmt == UNCOMPRESSED:
        payload = priv_key_raw
    else:
        raise Exception('Invalid Public Key format: %s' % key_fmt)
    return Base58.base58check(prefix, payload)
