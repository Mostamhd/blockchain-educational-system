from blockchain.pow.proof_of_work import ProofOfWork
from blockchain.block import Block
from blockchain.utils.helpers import BlockchainUtils
import threading
import time

class TestPoWConsensus:
    def test_mine_valid_block(self):
        engine = ProofOfWork()
        diff = 1
        
        block = Block([], "last_hash", "forger", 1)
        
        mined_block = engine.mine(block, diff)
        
        assert mined_block is not None
        assert mined_block.nonce >= 0
        
        assert engine.validate(mined_block, diff)

    def test_validate_valid_pow(self):
        engine = ProofOfWork()
        diff = 1
        
        block = Block([], "last_hash", "forger", 1)
        mined_block = engine.mine(block, diff)
        
        assert engine.validate(mined_block, diff)

    def test_validate_invalid_pow(self):
        engine = ProofOfWork()
        diff = 5 
        block = Block([], "last_hash", "forger", 1)
        
        assert not engine.validate(block, diff)

    def test_abort_mining(self):
        engine = ProofOfWork()
        diff = 10 
        block = Block([], "last_hash", "forger", 1)
        abort_event = threading.Event()
        
        def target():
            time.sleep(0.1)
            abort_event.set()
            
        t = threading.Thread(target=target)
        t.start()
        
        start_time = time.time()
        result = engine.mine(block, diff, abort_event)
        end_time = time.time()
        
        t.join()
        
        assert result is None
        assert (end_time - start_time) < 2.0