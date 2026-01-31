from blockchain.blockchain import Blockchain
from blockchain.block import Block
from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils
import time

class TestDifficultyAdjustment:
    def test_difficulty_increase(self):
        chain = Blockchain()
        chain.difficulty_adjustment_interval = 2
        chain.block_time = 10
        chain.difficulty = 1.0
        wallet = Wallet()
        
        genesis_time = chain.blocks[0].timestamp
        
        block1 = Block([], chain.blocks[-1].hash, wallet.public_key_string(), 1)
        block1.timestamp = genesis_time + 1
        chain.add_block(block1)
        
        old_diff = chain.difficulty
        new_diff = chain.adjust_difficulty()
        
        assert new_diff > old_diff
        assert new_diff == old_diff + 0.1

    def test_difficulty_decrease(self):
        chain = Blockchain()
        chain.difficulty_adjustment_interval = 2
        chain.block_time = 10
        chain.difficulty = 5.0 
        
        wallet = Wallet()
        genesis_time = chain.blocks[0].timestamp
        
        block1 = Block([], chain.blocks[-1].hash, wallet.public_key_string(), 1)
        block1.timestamp = genesis_time + 100
        chain.add_block(block1)
        
        old_diff = chain.difficulty
        new_diff = chain.adjust_difficulty()
        
        assert new_diff < old_diff
        assert new_diff == old_diff - 0.1
