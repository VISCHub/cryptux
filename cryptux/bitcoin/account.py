from binascii import hexlify

from ecdsa import SigningKey, VerifyingKey, SECP256k1

from .wif import priv_key_to_wif
from .gen_addr import bitcoin_addr_from_priv_key_hex


class Account(object):
    '''Represents a Bitcoin account'''

    def __init__(self, priv_key_raw, network_type, key_fmt):
        '''Create a Bitcoin account from private key'''
        self.signing_key = SigningKey.from_string(
            priv_key_raw, curve=SECP256k1)
        self.priv_key_raw = priv_key_raw
        self.network_type = network_type
        self.key_fmt = key_fmt

    @property
    def wif(self):
        '''Return WIF for the Private Key - read only property'''
        return priv_key_to_wif(self.priv_key_raw,
                               self.network_type, self.key_fmt)

    @property
    def hex(self):
        '''Return the Private Key in HEX - read only property'''
        return hexlify(self.priv_key_raw)

    @property
    def address(self):
        '''Bitcoin address based on details provided'''
        priv_key_hex = hexlify(self.priv_key_raw)
        return bitcoin_addr_from_priv_key_hex(
            priv_key_hex, self.network_type, self.key_fmt)

    @property
    def verbose_address(self):
        '''Returns verbose Bitcoin address'''
        return (self.address, self.network_type, self.key_fmt)
