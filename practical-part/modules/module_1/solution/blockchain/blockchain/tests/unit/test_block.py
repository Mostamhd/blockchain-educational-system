from blockchain.block import Block


class TestObjectBlocks:
    def test_initial_values(self, transaction_pool):
        p = transaction_pool["pool"]
        txs = p.transactions
        prev = "last_hash"
        f = "forger"
        h = 1
        
        obj = Block(txs, prev, f, h)
        
        dat = obj.to_dict()
        assert dat["block_height"] == 1
        assert dat["transactions"][0]["sender_public_key"]
        assert dat["forger"] == "forger"
        assert dat["last_hash"] == "last_hash"
