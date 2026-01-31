from blockchain.block import Block


class TestBlockData:
    def test_initialization(self, transaction_pool):
        p = transaction_pool["pool"]
        items = p.transactions
        prev = "last_hash"
        f = "forger"
        num = 1
        
        b = Block(items, prev, f, num)
        
        d = b.to_dict()
        assert d["block_height"] == 1
        assert d["transactions"][0]["sender_public_key"]
        assert d["forger"] == "forger"
        assert d["last_hash"] == "last_hash"
