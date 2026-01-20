import re
import logging

class InvalidTransactionError(Exception):
    pass

# Task 2: Schema Enforcement
# The node must reject transactions that try to store raw data instead of pointers.

def validate_transaction_payload(transaction):
    """
    Validates that 'STORE_FILE' transactions contain a valid SHA-256 hash pointer.
    """
    
    tx_type = transaction.get("type")
    tx_data = transaction.get("data", "")

    if tx_type == "STORE_FILE":
        print(f"[Protocol] Inspecting STORE_FILE payload: '{tx_data}'")
        
        # 1. Check if payload is empty
        if not tx_data:
            raise InvalidTransactionError("Storage transaction missing data payload.")

        # 2. Regex Validation for SHA-256 Hex String
        # Pattern: Exactly 64 characters, a-f, 0-9.
        sha256_pattern = r'^[a-fA-F0-9]{64}$'
        
        if not re.match(sha256_pattern, tx_data):
            logging.error("Validation Failed: Data is not a valid SHA-256 hash.")
            raise InvalidTransactionError(
                "Protocol Violation: Storage transactions must contain a valid 64-char SHA-256 hash."
            )
            
        print("[Protocol] Schema Validation Passed: Valid Hash Pointer detected.")
        return True
    
    return True # Other transaction types pass this specific check
