# https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses
# https://github.com/warner/python-ecdsa
# https://docs.python.org/3/library/hashlib.html
# Terminal: openssl ecparam -list_curves | grep -i secp256k1

from ecdsa import SigningKey, SECP256k1
from binascii import hexlify, unhexlify
from .constants import UNCOMPRESSED, COMPRESSED, MAINNET, TESTNET
from .constants import PUBKEY, PRIVKEY, P2SH
from cryptux.bitcoin.constants import NETWORK_TYPES
from cryptux.bitcoin.hashes import hash160, hash256
from .base58 import Base58

# http://www.secg.org/sec1-v2.pdf - Section 2.3.3
# https://tools.ietf.org/html/rfc5480 - Section 2.2
# Public Key Encoding
#   Compressed (32 bytes):
#     + y-coordinate is even: 0x02 || x-coordinate
#     + y-coordinate is odd:  0x03 || x-coordinate
#   Uncompressed (65 bytes):  0x04 || x-coordinate || y-coordinate

# Private Key Encoding for Bitcoin WIF
#   Uncompressed: No padding
#   Compressed:   Append 0x01 to the private key

# Extra: https://github.com/Legrandin/pycryptodome

# https://en.bitcoin.it/wiki/Base58Check_encoding
# Pay-to-script-hash (p2sh):
#   payload is: RIPEMD160(SHA256(redeemScript))
#   where redeemScript is a script the wallet knows how to spend;
#   version 0x05 (these addresses begin with the digit '3')
# Pay-to-pubkey-hash (p2pkh):
#   payload is RIPEMD160(SHA256(ECDSA_publicKey))
#   where ECDSA_publicKey is a public key the wallet knows the private key for;
#   version 0x00 (these addresses begin with the digit '1')


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
    COMPRESSED: get_compressed_pub_key,
    UNCOMPRESSED: get_uncompressed_pub_key,
}


def guess_wif_details(priv_key_wif):
    '''Deduce details of WIF private key'''
    # https://en.bitcoin.it/wiki/List_of_address_prefixes
    if priv_key_wif[0] == '5':
        return {'network_type': MAINNET, 'key_fmt': UNCOMPRESSED}
    elif priv_key_wif[0] in ['K', 'L']:
        return {'network_type': MAINNET, 'key_fmt': COMPRESSED}
    elif priv_key_wif[0] == '9':
        return {'network_type': TESTNET, 'key_fmt': UNCOMPRESSED}
    elif priv_key_wif[0] == 'c':
        return {'network_type': TESTNET, 'key_fmt': COMPRESSED}
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
    decoded_wif = Base58.to_base256(priv_key_wif)
    # Verify the WIF string
    if key_fmt == COMPRESSED:
        assert len(decoded_wif) == 38
        network_prefix, priv_key_raw = decoded_wif[0:1], decoded_wif[1:33]
        padding, checksum = decoded_wif[33:34], decoded_wif[34:]
        payload = decoded_wif[:34]
        assert padding == b'\x01'
    elif key_fmt == UNCOMPRESSED:
        assert len(decoded_wif) == 37
        payload = decoded_wif[:33]
        checksum = decoded_wif[33:]
        network_prefix, priv_key_raw = payload[:1], payload[1:]
    else:
        raise Exception('Invalid key format: %s' % key_fmt)
    assert network_prefix == NETWORK_TYPES[network_type][PRIVKEY]
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
    version = NETWORK_TYPES[network_type][PUBKEY]

    # Use Base58Check to obtain address
    bitcoin_addr = Base58.base58check(version, vk_hash160)
    return bitcoin_addr


def verify_bitcoin_addr(bitcoin_addr):
    '''Verify Bitcoin address'''
    bitcoin_addr_raw = Base58.to_base256(bitcoin_addr)
    assert len(bitcoin_addr_raw) == 25
    fmt_pubkey_hash = bitcoin_addr_raw[:21]
    checksum_4bytes = bitcoin_addr_raw[21:]

    # Verify that the double SHA-256 has the same prefix as checksum_4bytes
    full_checksum = hash256(fmt_pubkey_hash)
    return checksum_4bytes == full_checksum[:4]


def p2sh_addr_raw(redeem_script_raw, network_type):
    '''Pay-to-script-hash address. redeem_script_raw is a raw string'''
    version = NETWORK_TYPES[network_type][P2SH]
    payload = hash160(redeem_script_raw)
    return Base58.base58check(version, payload)


def p2sh_addr_hex(redeem_script_hex, network_type):
    '''Pay-to-script-hash address. redeem_script_hex is a hex string'''
    return p2sh_addr_raw(unhexlify(redeem_script_hex), network_type)
