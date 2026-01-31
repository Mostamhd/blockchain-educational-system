from blockchain.block import Block


class TestBlockStructure:
    def test_block_attributes_initialization(self, transaction_pool):
        pool_instance = transaction_pool["pool"]
        tx_list = pool_instance.transactions
        dummy_hash = "last_hash"
        miner_id = "forger"
        height_val = 1
        
        new_block = Block(tx_list, dummy_hash, miner_id, height_val)
        
        serialized_block = new_block.to_dict()
        assert serialized_block["block_height"] == 1
        assert serialized_block["transactions"][0]["sender_public_key"]
        assert serialized_block["forger"] == "forger"
        assert serialized_block["last_hash"] == "last_hash"