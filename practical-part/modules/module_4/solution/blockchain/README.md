# Module 4 Solution: Blockchain Digital Assets

This directory contains the solution for Module 4, implementing digital assets (Books) on a Proof of Stake blockchain.

## Implemented Tasks

### Task 1: Hello World Transaction
- Modified `Transaction` class to accept arbitrary data.
- Updated API to handle data payloads.
- **Verification:** Transactions can now carry text strings like "Hello Blockchain".

### Task 2: Asset Schema
- Created `Book` class in `digital_asset.py`.
- Attributes: `isbn`, `title`, `author`, `owner_public_key`.
- Serialization: `to_json()` method for storing book data on-chain.

### Task 3: Library Management System
- **Registration:** `register_book.py` creates a book and registers it on the blockchain.
- **Transfer:** `transfer_book.py` updates the owner of a book via a new transaction.
- **Validation:** Scripts demonstrate the full lifecycle of a digital asset.

## Usage

### 1. Start the Network
```bash
docker-compose up --build
```

### 2. Register a Book
```bash
python register_book.py
```

### 3. Transfer a Book
```bash
python transfer_book.py
```
