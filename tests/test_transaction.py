import pytest

from blockchain.block import Transaction


@pytest.fixture
def txn_no_witness():
    """Transaction without segwit support"""
    txn = (
        '0100000001b3e128f5b0eac3f7450bb917bbde0386ff0f9abee1ddf515a4cb134626f'
        '19995000000006a47304402206875ff49147241ce61f9dabfd7ae665b04d435a994e3'
        '4bc5af791002a26bdc33022051e969188a5eb4d8dbe3f964f27f81be100f6f48036c9'
        '9cdc3449831dcc42db30121025a5b2d0dd49199e106ea16438ec8792a2f30d8855d64'
        '1029c6f8c340a05a2881ffffffff0279729300000000001976a914aad93c59fb62e5b'
        '7b1e8fd40b8b848dbb5897ab988ac80f0fa02000000001976a914baa64eadb3ea26ec'
        '2f721b3e1b43ed3ef95ffca188ac00000000'
    )
    return bytes.fromhex(txn)


@pytest.fixture
def txn_with_witness():
    """Transaction with 2 witness stack items for the first input"""
    txn = (
        '0100000000010115e180dc28a2327e687facc33f10f2a20da717e5548406f7ae8b4c8'
        '11072f856040000002322002001d5d92effa6ffba3efa379f9830d0f75618b1339382'
        '7152d26e4309000e88b1ffffffff0188b3f505000000001976a9141d7cd6c75c2e86f'
        '4cbf98eaed221b30bd9a0b92888ac02473044022038421164c6468c63dc7bf724aa9d'
        '48d8e5abe3935564d38182addf733ad4cd81022076362326b22dd7bfaf211d5b17220'
        '723659e4fe3359740ced5762d0e497b7dcc012321038262a6c6cec93c2d3ecd6c6072'
        'efea86d02ff8e3328bbd0242b20af3425990acac00000000'
    )
    return bytes.fromhex(txn)


def test_tx_no_witness(txn_no_witness):
    txn, _ = Transaction.from_binary_data(txn_no_witness, 0, 0)
    assert txn.version == 1
    assert all(inp.witness_stack_items is None for inp in txn.inputs)
    assert txn.txn_hash == '8af1c511ec4ac9891e70a550ec3e176c68358f69821a1bd9356f4c57ea8474ab'


def test_tx_with_witness(txn_with_witness):
    tx, _ = Transaction.from_binary_data(txn_with_witness, 0, 0)
    assert tx.version == 1
    assert len(tx.inputs[0].witness_stack_items) == 2
    assert [wsi.hex() for wsi in tx.inputs[0].witness_stack_items] == [
        '3044022038421164c6468c63dc7bf724aa9d48d8e5abe3935564d38182addf733ad4cd81022076362326b22dd7bfaf211d5b17220723659e4fe3359740ced5762d0e497b7dcc01',
        '21038262a6c6cec93c2d3ecd6c6072efea86d02ff8e3328bbd0242b20af3425990acac']
    assert tx.txn_hash == '954f43dbb30ad8024981c07d1f5eb6c9fd461e2cf1760dd1283f052af746fc88'
