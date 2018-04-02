#!/usr/bin/env python3

# https://bitcoin.stackexchange.com/questions/56520/how-to-generate-a-testnet-address
# https://www.bitaddress.org/?testnet=true

import cryptux.bitcoin.constants as BCONST
from cryptux.bitcoin.gen_addr import bitcoin_addr_from_priv_key_wif
from cryptux.bitcoin.gen_addr import bitcoin_addr_from_priv_key_hex
from cryptux.bitcoin.gen_addr import p2sh_addr_hex
from cryptux.bitcoin.gen_addr import verify_bitcoin_addr

TEST_CASES_HEX = [
    {
        'priv':
        '18E14A7B6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725',
        'addr':
        '16UwLL9Risc3QfPqBUvKofHmBQ7wMtjvM',
        'key_fmt':
        BCONST.UNCOMPRESSED,
        'network_type':
        BCONST.MAINNET,
    },
]

TEST_CASES_WIF = [
    {
        'priv': 'L3BQRZyUzNPUPbt1HtGby9UwVb5iz2RyEk9jQk1vqhnL5CwFZHiX',
        'addr': '1D2Gme2513ncWsxB4DchzT3ukeNUXYVv3c',
    },
    {
        'priv': 'KweM5soEt19VNn2T5yVATkqQAGse51djuxBhyewvra3tqtbvmW3z',
        'addr': '1HTgPiqjeTUcj8epgF3YW1HGAU2zbps1wY',
    },
    {
        'priv': '5Kb8kLf9zgWQnogidDA76MzPL6TsZZY36hWXMssSzNydYXYB9KF',
        'addr': '1CC3X2gu58d6wXUWMffpuzN9JAfTUWu4Kj',
    },
    {
        'priv': '92Hfa6Zfs7g3wB6B1wPdNhYHzbtnK4rPTriWU4ADWuQjADcUmox',
        'addr': 'mwC4ik7crQMXWYwWMQxJciZzTWVWYzfwbN',
    },
    {
        'priv': 'cSDWGTNWzNtLzJE5SspMeKT4w6gKcGnsP2USGaM87p1rpD6VF5b9',
        'addr': 'mn9DYsMDMrSkRK3jedNhMwPpBcQ5JyrXAb',
    },
    {
        'priv': 'L5DWDzHGBzTUU6uEXDWMCiSfacys1z2y4sFznPnFAzstJ3KkHix4',
        'addr': '15LsCQHu4kPXxb9maM3cfnQHSpPPFzbr7p',
    },
]

# https://github.com/anders94/bitcoin-2-of-3-multisig
TEST_CASES_REDEEM_SCRIPT_HEX = [
    {
        'redeemScript': '524104a97b658c114d77dc5f71736ab78fbe408ce632ed1478d7eaa106eef67c55d58a91c6449de4858faf11721e85fe09ec850c6578432eb4be9a69c76232ac593c3b4104019ef04a316792f0ecbe5ab1718c833c3964dee3626cfabe19d97745dbcaa5198919081b456e8eeea5898afa0e36d5c17ab693a80d728721128ed8c5f38cdba04104a04f29f308160e6f945b33d943304b1b471ed8f9eaceeb5412c04e60a0fab0376871d9d1108948b67cafbc703e565a18f8351fb8558fd7c7482d7027eecd687c53ae',
        'addr': '38aNB81yPqNp6X2T3rXYZN8Z3C4pSbqEvs',
        'network_type': BCONST.MAINNET,
    },
]


def test_gen_addr_from_priv_key_wif():
    '''Test Bitcoin address generation from private keys in WIF'''
    for test_case in TEST_CASES_WIF:
        print('Verifying the case: ', test_case)
        priv_key_wif = test_case['priv']
        bitcoin_addr = bitcoin_addr_from_priv_key_wif(priv_key_wif)
        assert bitcoin_addr == test_case['addr']
        assert verify_bitcoin_addr(bitcoin_addr)
        print('This case was successful!')


def test_gen_addr_from_priv_key_hex():
    '''Test Bitcoin address generation from private keys in HEX'''
    for test_case in TEST_CASES_HEX:
        print('Verifying the case: ', test_case)
        priv_key_hex = test_case['priv']
        key_fmt = test_case['key_fmt']
        network_type = test_case['network_type']
        bitcoin_addr = bitcoin_addr_from_priv_key_hex(priv_key_hex,
                                                      network_type, key_fmt)
        assert bitcoin_addr == test_case['addr']
        assert verify_bitcoin_addr(bitcoin_addr)
        print('This case was successful!')


def test_gen_add_from_redeem_script_hex():
    '''Test Bitcoin address generation from redeemScript in HEX'''
    for test_case in TEST_CASES_REDEEM_SCRIPT_HEX:
        print('Verifying the case: ', test_case)
        redeem_script_hex = test_case['redeemScript']
        network_type = test_case['network_type']
        bitcoin_addr = p2sh_addr_hex(redeem_script_hex, network_type)
        assert bitcoin_addr == test_case['addr']
        assert verify_bitcoin_addr(bitcoin_addr)
        print('This case was successful!')
