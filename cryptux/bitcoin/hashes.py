import hashlib


def hash160(in_bytes):
    '''Performs RIPEMD160(SHA256(in_bytes)) and returns raw digest'''
    ripemd160_hasher = hashlib.new('ripemd160')
    ripemd160_hasher.update(hashlib.sha256(in_bytes).digest())
    return ripemd160_hasher.digest()


def hash256(in_bytes):
    '''Performs SHA256(SHA256(in_bytes)) and returns raw digest'''
    sha256 = hashlib.sha256
    return sha256(sha256(in_bytes).digest()).digest()
