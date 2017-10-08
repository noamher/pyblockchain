from tempfile import NamedTemporaryFile

import pytest
from blockchain.reader import BlockchainFileReader

@pytest.fixture
def genesis_block():
    """https://en.bitcoin.it/wiki/Genesis_block"""
    genesis_block_hex = (
        'f9beb4d91d01000001000000000000000000000000000000000000000000000000000'
        '00000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a'
        '9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c0101000000010000000000000000000'
        '000000000000000000000000000000000000000000000ffffffff4d04ffff001d0104'
        '455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206'
        'f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b'
        '73ffffffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd'
        '6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7'
        'ba0b8d578a4c702b6bf11d5fac00000000'
    )
    return bytes.fromhex(genesis_block_hex)


def test_read_single_block_file(genesis_block):
    with NamedTemporaryFile() as block_file:
        block_file.write(genesis_block)
        block_file.flush()
        it = iter(BlockchainFileReader(block_file.name))
        next(it)
        try:
            next(it)
            pytest.fail('exception should have been thrown')
        except StopIteration: pass