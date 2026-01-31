from blockchain.blockchain import Blockchain
from blockchain.utils.helpers import BlockchainUtils
from blockchain.transaction.wallet import Wallet


class TestMainChain:
    def test_block_addition(self, transaction_pool):
        w = transaction_pool["transaction_from_wallet"]["wallet"]
        p = transaction_pool["pool"]

        b = w.create_block(p.transactions, "last_hash", 1)

        inst = Blockchain()
        inst.add_block(b)

        dat = inst.to_dict()

        assert len(dat["blocks"]) == 2
        assert dat["blocks"][0]["last_hash"] == "genesis_group_05"

    def test_integrity_checks(self, transaction_pool):
        w = transaction_pool["transaction_from_wallet"]["wallet"]
        p = transaction_pool["pool"]

        inst = Blockchain()

        lh = BlockchainUtils.hash(inst.blocks[-1].payload()).hex()
        nxt = inst.blocks[-1].block_height + 1
        
        b_ok = w.create_block(p.transactions, lh, nxt)
        assert inst.last_block_hash_valid(b_ok)
        assert inst.block_count_valid(b_ok)

        b_err = w.create_block(p.transactions, lh, nxt + 10)
        assert not inst.block_count_valid(b_err)

        inst.add_block(b_ok)
        
        dat = inst.to_dict()
        assert dat["blocks"]
        assert dat["blocks"][0]["last_hash"] == "genesis_group_05"

    def test_tx_lookup(self):
        inst = Blockchain()
        u1 = Wallet()
        u2 = Wallet()
        
        tx = u1.create_transaction(u2.public_key_string(), 5, "TRANSFER")
        
        assert not inst.transaction_exists(tx)
        
        m = Wallet()
        lh = BlockchainUtils.hash(inst.blocks[-1].payload()).hex()
        b = m.create_block([tx], lh, 1)
        
        inst.add_block(b)
        
        assert inst.transaction_exists(tx)
