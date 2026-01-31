import pytest
import json
import re
from blockchain.blockchain import Blockchain
from blockchain.transaction.transaction import Transaction
from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils

class TestModule5Tasks:

    def test_max_block_size_enforcement(self):
        bc = Blockchain()
        
        wallet = Wallet()
        receiver = Wallet()
        
        tx_small = wallet.create_transaction(receiver.public_key_string(), 1, "EXCHANGE")
        tx_small_size = len(BlockchainUtils.encode(tx_small))
        
        bc.max_block_size = tx_small_size + 10 
        
        large_data = "x" * 2000
        tx_large = wallet.create_transaction(receiver.public_key_string(), 0, "EXCHANGE", data=large_data)
        tx_large_size = len(BlockchainUtils.encode(tx_large))
        
        transactions = [tx_small, tx_large]
        
        block = bc.create_block(transactions, wallet)
        
        print(f"Small TX size: {tx_small_size}, Large TX size: {tx_large_size}, Limit: {bc.max_block_size}")
        
        assert len(block.transactions) == 1
        assert block.transactions[0].id == tx_small.id
        
        included_size = len(BlockchainUtils.encode(tx_small))
        assert included_size <= bc.max_block_size

    def test_store_file_schema_validation(self):
        bc = Blockchain()
        wallet = Wallet()
        
        valid_hash = "a" * 64
        tx_valid = wallet.create_transaction(wallet.public_key_string(), 0, "STORE_FILE", data=valid_hash)
        assert bc.transaction_covered(tx_valid) is True
        
        invalid_hash_short = "a" * 63
        tx_invalid_short = wallet.create_transaction(wallet.public_key_string(), 0, "STORE_FILE", data=invalid_hash_short)
        assert bc.transaction_covered(tx_invalid_short) is False
        
        invalid_hash_long = "a" * 65
        tx_invalid_long = wallet.create_transaction(wallet.public_key_string(), 0, "STORE_FILE", data=invalid_hash_long)
        assert bc.transaction_covered(tx_invalid_long) is False
        
        invalid_hash_chars = "g" * 64
        tx_invalid_chars = wallet.create_transaction(wallet.public_key_string(), 0, "STORE_FILE", data=invalid_hash_chars)
        assert bc.transaction_covered(tx_invalid_chars) is False
        
        tx_no_data = wallet.create_transaction(wallet.public_key_string(), 0, "STORE_FILE", data=None)
        assert bc.transaction_covered(tx_no_data) is False

    def test_default_max_block_size(self):
        bc = Blockchain()
        assert bc.max_block_size == 102400
