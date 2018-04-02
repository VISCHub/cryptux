import binascii
import sys
from cryptux.bitcoin.hashes import hash256

# https://www.bitaddress.org/
# https://github.com/pointbiz/bitaddress.org
# https://en.wikipedia.org/wiki/Base58

BASE58_CHARS = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def map_base58():
    '''Create a map of chars for Base58'''
    tmp_dir = {}
    i = 0
    for c in BASE58_CHARS:
        tmp_dir[c] = i
        i = i + 1
    return tmp_dir


BASE58_MAP = map_base58()


def base58_enc(in_num):
    '''Encode a number into Bitcoin Base58 format'''
    if in_num < 0:
        raise Exception("Positive integers only")
    tmp_out = []
    while in_num > 0:
        tmp_out.append(BASE58_CHARS[in_num % 58])
        in_num = in_num // 58
    tmp_out.reverse()
    return ''.join(tmp_out)


def base256_to_base58_py3(raw_bytes):
    '''Convert a raw string to Base58 string. For Python 3'''
    leading_zeros = 0
    num = 0
    for c in raw_bytes:
        if c != 0:
            break
        leading_zeros = leading_zeros + 1
    for c in raw_bytes:
        num = num * 256 + c
    base58_str = ''.join(leading_zeros * ['1']) + base58_enc(num)
    return base58_str


def base256_to_base58_py2(raw_bytes):
    '''Convert a raw string to Base58 string. For Python 2'''
    leading_zeros = 0
    num = 0
    for c in raw_bytes:
        if c != '\x00':
            break
        leading_zeros = leading_zeros + 1
    for c in raw_bytes:
        num = num * 256 + ord(c)
    base58_str = ''.join(leading_zeros * ['1']) + base58_enc(num)
    return base58_str


class Base58(object):
    '''Wraps Base58 related functions'''

    @staticmethod
    def encode(in_num):
        '''Encode a number into Bitcoin Base58 format'''
        return base58_enc(in_num)

    @staticmethod
    def decode(in_bytes):
        '''Decode a Bitcoin Base58 string to a number'''
        out_num = 0
        for c in in_bytes:
            if c not in BASE58_MAP:
                raise Exception("Invalid char, not in Base58: %c" % c)
            out_num = out_num * 58 + BASE58_MAP[c]
        return out_num

    @staticmethod
    def from_base256(raw_bytes):
        '''Convert a raw string to Base58 string'''
        if sys.version_info[0] < 3:
            return base256_to_base58_py2(raw_bytes)
        return base256_to_base58_py3(raw_bytes)

    @staticmethod
    def to_base256(base58_str):
        '''Convert a Base58 string to raw string'''
        leading_ones = 0
        for c in base58_str:
            if c != '1':
                break
            leading_ones = leading_ones + 1
        num = Base58.decode(base58_str)
        raw_str_suffix_hex = '%02x' % num
        if len(raw_str_suffix_hex) % 2:
            raw_str_suffix_hex = '0%s' % raw_str_suffix_hex
        raw_str_hex = ''.join(leading_ones * ['00']) + raw_str_suffix_hex
        raw_bytes = binascii.unhexlify(raw_str_hex)
        return raw_bytes

    @staticmethod
    def base58check(version, payload):
        '''Implements Base58Check standard function. The payload must be 160 bit'''
        # Add version byte in front of RIPEMD-160 hash (0x00 for Main Network)
        combined_payload = version + payload

        # Perform SHA-256 hash on the extended RIPEMD-160 result
        # Perform SHA-256 hash on the result of the previous SHA-256 hash
        full_checksum = hash256(combined_payload)

        # Take the first 4 bytes of the second SHA-256 hash
        # This is the address checksum
        checksum_4bytes = full_checksum[:4]

        # Add the 4 checksum bytes from stage 7 at the end of
        # extended RIPEMD-160 hash from stage 4.
        base58cksum_raw = combined_payload + checksum_4bytes
        # Bitcoin Address should have length of 25 bytes
        # assert len(base58cksum_raw) == 25

        # Convert the result from a byte string into a base58 string
        # using Base58Check encoding.
        # This is the most commonly used Bitcoin Address format
        base58cksum = Base58.from_base256(base58cksum_raw)
        # Quick validation
        base58cksum_raw_again = Base58.to_base256(base58cksum)
        assert base58cksum_raw_again == base58cksum_raw
        return base58cksum
