import json
import logging

# Task 1: Protocol Defense
# Defining a hard limit on block size to prevent network DoS/Bloat.
MAX_BLOCK_SIZE_BYTES = 2048  # 2KB Limit for this educational module

class BlockSizeExceededError(Exception):
    pass

class Blockchain:
    def __init__(self):
        self.chain = []

    def to_dict(self):
        return [block.to_dict() for block in self.chain]

    def add_block(self, block):
        """
        Adds a block to the chain ONLY if it meets protocol constraints.
        """
        
        # 1. Serialize the block to measure its actual transmission size
        # We use ensure_ascii=False to get the actual byte length representation
        block_payload = json.dumps(block.to_dict(), ensure_ascii=False).encode('utf-8')
        payload_size = len(block_payload)
        
        print(f"[Protocol] Validating Block Size: {payload_size} bytes...")

        # 2. Enforce the Limit
        if payload_size > MAX_BLOCK_SIZE_BYTES:
            err_msg = (f"Block rejected! Size {payload_size}B exceeds "
                       f"protocol limit of {MAX_BLOCK_SIZE_BYTES}B")
            logging.error(err_msg)
            raise BlockSizeExceededError(err_msg)
            
        # 3. If valid, append (Simulated)
        self.chain.append(block)
        print(f"[Protocol] Block accepted. (Height: {len(self.chain)})")
        return True
