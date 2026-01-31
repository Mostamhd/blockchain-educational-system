from blockchain.blockchain import Blockchain
from blockchain.utils.helpers import BlockchainUtils
from blockchain.transaction.wallet import Wallet


class TestChainLogic:
    def test_block_insertion(self, transaction_pool):
        w = transaction_pool["transaction_from_wallet"]["wallet"]
        p = transaction_pool["pool"]

        b = w.create_block(p.transactions, "last_hash", 1)

        c = Blockchain()
        c.add_block(b)

        res = c.to_dict()

        assert len(res["blocks"]) == 2
        assert res["blocks"][0]["last_hash"] == "genesis_block"

    def test_validation_rules(self, transaction_pool):
        w = transaction_pool["transaction_from_wallet"]["wallet"]
        p = transaction_pool["pool"]

        c = Blockchain()

        lh = BlockchainUtils.hash(c.blocks[-1].payload()).hex()
        nxt = c.blocks[-1].block_height + 1
        
        b_ok = w.create_block(p.transactions, lh, nxt)
        assert c.last_block_hash_valid(b_ok)
        assert c.block_count_valid(b_ok)

        b_err = w.create_block(p.transactions, lh, nxt + 10)
        assert not c.block_count_valid(b_err)

        c.add_block(b_ok)
        
        res = c.to_dict()
        assert res["blocks"]
        assert res["blocks"][0]["last_hash"] == "genesis_block"

    def test_tx_presence(self):
        c = Blockchain()
        u1 = Wallet()
        u2 = Wallet()
        
        t = u1.create_transaction(u2.public_key_string(), 5, "TRANSFER")
        
        assert not c.transaction_exists(t)
        
        m = Wallet()
        lh = BlockchainUtils.hash(c.blocks[-1].payload()).hex()
        b = m.create_block([t], lh, 1)
        
        c.add_block(b)
        
        assert c.transaction_exists(t)
