# https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses
# https://github.com/warner/python-ecdsa
# https://docs.python.org/3/library/hashlib.html
# Terminal: openssl ecparam -list_curves | grep -i secp256k1

from ecdsa import SigningKey, SECP256k1
from binascii import hexlify

from . import constants as BCONST
from .constants import NETWORK_TYPES
from .hashes import hash160, hash256
from .base58 import base58_to_base256, base58check


def get_compressed_pub_key(pub_key_raw):
    '''Represent public key in the compressed format'''
    assert len(pub_key_raw) == 64
    p_x = pub_key_raw[:32]
    p_y = pub_key_raw[32:]
    p_y_num = int(hexlify(p_y), 16)
    prefix = b'\x03' if p_y_num % 2 else b'\x02'
    compressed_pub_key = prefix + p_x
    assert len(compressed_pub_key) == 33
    return compressed_pub_key


def get_uncompressed_pub_key(pub_key_raw):
    '''Represent public key in full/uncompressed format'''
    # (65 bytes, 1 byte 0x04, 32 bytes corresponding to X coordinate,
    # 32 bytes corresponding to Y coordinate)
    assert len(pub_key_raw) == 64
    full_pub_key = b'\x04' + pub_key_raw
    assert len(full_pub_key) == 65
    return full_pub_key


PUB_KEY_FORMATS = {
    BCONST.COMPRESSED: get_compressed_pub_key,
    BCONST.UNCOMPRESSED: get_uncompressed_pub_key,
}


def guess_wif_details(priv_key_wif):
    '''Deduce details of WIF private key'''
    # https://en.bitcoin.it/wiki/List_of_address_prefixes
    if priv_key_wif[0] == '5':
        return {'network_type': BCONST.MAINNET, 'key_fmt': BCONST.UNCOMPRESSED}
    elif priv_key_wif[0] in ['K', 'L']:
        return {'network_type': BCONST.MAINNET, 'key_fmt': BCONST.COMPRESSED}
    elif priv_key_wif[0] == '9':
        return {'network_type': BCONST.TESTNET, 'key_fmt': BCONST.UNCOMPRESSED}
    elif priv_key_wif[0] == 'c':
        return {'network_type': BCONST.TESTNET, 'key_fmt': BCONST.COMPRESSED}
    else:
        raise Exception('Unhandled WIF format')


def pub_key_from_priv_key_hex(priv_key_hex):
    '''Obtain public key from the private key in HEX'''
    secexp = int(priv_key_hex, 16)
    signing_key = SigningKey.from_secret_exponent(secexp, curve=SECP256k1)
    vk = signing_key.get_verifying_key()
    return vk.to_string()


def bitcoin_addr_from_priv_key_hex(priv_key_hex, network_type, key_fmt):
    '''Create Bitcoin address from the private key in HEX'''
    # Generate ECDSA public key from the private key
    pub_key_raw = pub_key_from_priv_key_hex(priv_key_hex)
    pub_key_formatted = PUB_KEY_FORMATS[key_fmt](pub_key_raw)
    return bitcoin_addr_from_pub_key(pub_key_formatted, network_type)


def priv_key_from_wif(priv_key_wif):
    '''Extract raw private key from the WIF string'''
    wif_details = guess_wif_details(priv_key_wif)
    network_type = wif_details['network_type']
    key_fmt = wif_details['key_fmt']
    decoded_wif = base58_to_base256(priv_key_wif)
    # Verify the WIF string
    if key_fmt == BCONST.COMPRESSED:
        assert len(decoded_wif) == 38
        network_prefix, priv_key_raw = decoded_wif[0:1], decoded_wif[1:33]
        padding, checksum = decoded_wif[33:34], decoded_wif[34:]
        payload = decoded_wif[:34]
        assert padding == b'\x01'
    elif key_fmt == BCONST.UNCOMPRESSED:
        assert len(decoded_wif) == 37
        payload = decoded_wif[:33]
        checksum = decoded_wif[33:]
        network_prefix, priv_key_raw = payload[:1], payload[1:]
    else:
        raise Exception('Invalid key format: %s' % key_fmt)
    assert network_prefix == NETWORK_TYPES[network_type][BCONST.PRIVKEY]
    assert hash256(payload)[:4] == checksum
    return (priv_key_raw, network_type, key_fmt)


def pub_key_from_priv_key_wif(priv_key_wif):
    '''Obtain public key from the private key in WIF'''
    # Obtain the raw public key from raw private key
    priv_key_raw, network_type, key_fmt = priv_key_from_wif(priv_key_wif)
    signing_key = SigningKey.from_string(priv_key_raw, curve=SECP256k1)
    vk = signing_key.get_verifying_key()
    pub_key_raw = vk.to_string()
    return (pub_key_raw, network_type, key_fmt)


def bitcoin_addr_from_priv_key_wif(priv_key_wif):
    '''Create Bitcoin address from the private key'''
    # Generate ECDSA public key from the private key
    pub_key_raw, network_type, key_fmt = pub_key_from_priv_key_wif(
        priv_key_wif)
    pub_key_formatted = PUB_KEY_FORMATS[key_fmt](pub_key_raw)
    return bitcoin_addr_from_pub_key(pub_key_formatted, network_type)


def bitcoin_addr_from_pub_key(pub_key_formatted, network_type):
    '''Create Bitcoin address from the public key'''
    # Perform SHA-256 hashing on the public key
    # Perform RIPEMD-160 hashing on the result of SHA-256
    vk_hash160 = hash160(pub_key_formatted)
    version = NETWORK_TYPES[network_type][BCONST.PUBKEY]

    # Use Base58Check to obtain address
    bitcoin_addr = base58check(version, vk_hash160)
    return bitcoin_addr


def verify_bitcoin_addr(bitcoin_addr):
    '''Verify Bitcoin address'''
    bitcoin_addr_raw = base58_to_base256(bitcoin_addr)
    assert len(bitcoin_addr_raw) == 25
    fmt_pubkey_hash = bitcoin_addr_raw[:21]
    checksum_4bytes = bitcoin_addr_raw[21:]

    # Verify that the double SHA-256 has the same prefix as checksum_4bytes
    full_checksum = hash256(fmt_pubkey_hash)
    return checksum_4bytes == full_checksum[:4]
