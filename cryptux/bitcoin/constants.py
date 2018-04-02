COMPRESSED = 'COMPRESSED'
UNCOMPRESSED = 'UNCOMPRESSED'
MAINNET = 'MAINNET'
TESTNET = 'TESTNET'
PUBKEY = 'PUBKEY'
PRIVKEY = 'PRIVKEY'
P2SH = 'P2SH'

NETWORK_TYPES = {
    MAINNET: {
        PUBKEY: b'\x00',
        PRIVKEY: b'\x80',
        P2SH: b'\x05',
    },
    TESTNET: {
        PUBKEY: b'\x6F',
        PRIVKEY: b'\xEF',
        P2SH: b'\xC4',
    },
}
