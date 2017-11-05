import hashlib


def hash160(in_bytes):
    '''Performs RIPEMD160(SHA256(in_bytes)) and returns raw digest'''
    sha256_hasher = hashlib.sha256(in_bytes)
    ripemd160_hasher = hashlib.new('ripemd160')
    ripemd160_hasher.update(sha256_hasher.digest())
    return ripemd160_hasher.digest()


def hash256(in_bytes):
    '''Performs SHA256(SHA256(in_bytes)) and returns raw digest'''
    sha256_hasher = hashlib.sha256(in_bytes)
    sha256_hasher2 = hashlib.sha256(sha256_hasher.digest())
    return sha256_hasher2.digest()
