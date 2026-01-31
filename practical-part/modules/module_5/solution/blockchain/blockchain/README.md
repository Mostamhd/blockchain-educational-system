# Module 5 Solution: System Extensibility and Design Challenge

This directory contains the solution for Module 5, focusing on architectural scalability, block size enforcement, and hybrid on-chain/off-chain storage patterns.

## Implemented Tasks

### Task 1: Enforcing Block Size Limits
- Defined `max_block_size` (100KB) in the `Blockchain` class.
- Implemented transaction selection logic in `create_block()` to ensure cumulative transaction size does not exceed the protocol limit.
- **Verification:** Nodes now exclude transactions from a block if including them would violate the size constraint, preventing unsustainable ledger growth.

### Task 2: Schema Enforcement (Hybrid Architecture)
- Implemented validation rules for the `STORE_FILE` transaction type.
- Enforced that `STORE_FILE` transactions must contain a valid 64-character SHA-256 hex string in the `data` field.
- **Verification:** This ensures the blockchain acts as an integrity layer for off-chain storage (like IPFS), storing only cryptographic pointers rather than raw binary data.

## Cumulative Features (from previous modules)
- **Proof of Stake Consensus:** Leader selection based on validator lots and stakes.
- **Digital Assets:** Registration and Transfer logic for `Book` assets (Module 4).
- **P2P Networking:** Automatic peer discovery and synchronization.

## Usage

### 1. Start the Network
```bash
docker-compose up --build
```

### 2. Testing Block Size Limits
You can modify `self.max_block_size` in `blockchain/blockchain.py` to a small value (e.g., 500) and attempt to send multiple transactions to see the enforcement in action.

### 3. Storing a File Hash
Submit a transaction with type `STORE_FILE` and a SHA-256 hash:
```json
{
  "transaction": {
    "sender": "...",
    "receiver": "...",
    "amount": 0,
    "type": "STORE_FILE",
    "data": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a1b2c3d4e5f6"
  }
}
```

## Running Tests
To verify the implementation of Module 5 tasks:
```bash
pytest tests/unit/test_module_5_tasks.py
```