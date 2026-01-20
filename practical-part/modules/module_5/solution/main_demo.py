import time
import hashlib
from blockchain import Blockchain, BlockSizeExceededError
from transaction_validator import validate_transaction_payload, InvalidTransactionError

# Mocking a Block class for the demo
class Block:
    def __init__(self, transactions):
        self.transactions = transactions
        self.timestamp = time.time()
    
    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "transactions": self.transactions
        }

def run_demo():
    print("=== Module 5: Protocol Engineering Demo ===\n")
    chain = Blockchain()

    # --- Scenario 1: The Bloated Block Attack ---
    print("--- Test 1: Attempting to mine a 'Bloated Block' (5KB) ---")
    
    # Create a large payload (simulating a user trying to upload a small image directly)
    bloated_tx = {"sender": "Alice", "data": "A" * 5000} 
    bloated_block = Block([bloated_tx])
    
    try:
        chain.add_block(bloated_block)
    except BlockSizeExceededError as e:
        print(f"SUCCESS: System successfully rejected the attack.\nReason: {e}\n")

    # --- Scenario 2: The Raw Data Transaction ---
    print("--- Test 2: Submitting Raw Text as a 'STORE_FILE' transaction ---")
    
    bad_tx = {
        "type": "STORE_FILE",
        "data": "This is just raw text, not a hash."
    }
    
    try:
        validate_transaction_payload(bad_tx)
    except InvalidTransactionError as e:
        print(f"SUCCESS: Validator rejected invalid schema.\nReason: {e}\n")

    # --- Scenario 3: The Valid Hybrid Transaction ---
    print("--- Test 3: Submitting a valid IPFS Hash ---")
    
    # Simulate IPFS Hash
    valid_hash = hashlib.sha256(b"My PDF Content").hexdigest()
    
    good_tx = {
        "type": "STORE_FILE",
        "data": valid_hash  # 64 chars hex
    }
    
    try:
        if validate_transaction_payload(good_tx):
            # If valid, wrap in block
            good_block = Block([good_tx])
            chain.add_block(good_block)
            print("SUCCESS: Valid Hybrid Block appended to chain.")
            
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    run_demo()
