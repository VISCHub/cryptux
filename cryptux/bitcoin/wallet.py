from .account import Account
from .gen_addr import priv_key_from_wif


class Wallet(object):
    '''Utility class to manage Bitcoin accounts'''

    @staticmethod
    def account_from_wif(wif):
        '''Creates a Bitcoin account from a WIF string'''
        (priv_key_raw, network_type, key_fmt) = priv_key_from_wif(wif)
        return Account(priv_key_raw, network_type, key_fmt)
