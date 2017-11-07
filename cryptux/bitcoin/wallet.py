from ecdsa import SigningKey, VerifyingKey, SECP256k1

from .account import Account
from .gen_addr import priv_key_from_wif
from .constants import MAINNET, COMPRESSED


class Wallet(object):
    '''Utility class to manage Bitcoin accounts'''

    @staticmethod
    def account_from_wif(wif):
        '''Creates a Bitcoin account from a WIF string'''
        (priv_key_raw, network_type, key_fmt) = priv_key_from_wif(wif)
        return Account(priv_key_raw, network_type, key_fmt)

    @staticmethod
    def gen_account(network_type=MAINNET, key_fmt=COMPRESSED):
        '''Generate a new Bitcoin account randomly'''
        sk = SigningKey.generate(curve=SECP256k1)
        priv_key_raw = sk.to_string()
        return Account(priv_key_raw, network_type, key_fmt)
