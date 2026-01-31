from blockchain.utils.helpers import BlockchainUtils

class ProofOfWork:
    def __init__(self):
        pass

    def calculate_target(self, difficulty):
        exponent = 256 - (4 * difficulty)
        
        if exponent < 0:
            exponent = 0
            
        return int(2 ** exponent)

    def mine(self, block, difficulty, abort_event=None):
        target = self.calculate_target(difficulty)

        block.nonce = 0
        while True:
            if abort_event and abort_event.is_set():
                return None 

            block_hash = BlockchainUtils.hash(block.payload()).hex()
            
            if int(block_hash, 16) < target:
                return block
            
            block.nonce += 1

    def validate(self, block, difficulty):
        target = self.calculate_target(difficulty)
        block_hash = BlockchainUtils.hash(block.payload()).hex()
        return int(block_hash, 16) < target