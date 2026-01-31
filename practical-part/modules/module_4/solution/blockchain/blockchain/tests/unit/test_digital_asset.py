from blockchain.transaction.digital_asset import Book
from blockchain.transaction.wallet import Wallet
from blockchain.transaction.transaction_pool import TransactionPool
from blockchain.blockchain import Blockchain
from blockchain.utils.helpers import BlockchainUtils
import json

class TestDigitalAssets:
    def test_book_model(self):
        wallet = Wallet()
        book = Book("978-3-16-148410-0", "Test Book", "Test Author", wallet.public_key_string())
        
        json_data = book.to_json()
        assert "978-3-16-148410-0" in json_data
        
        book_restored = Book.from_json(json_data)
        assert book_restored.isbn == book.isbn
        assert book_restored.owner_public_key == book.owner_public_key

    def test_asset_registration(self):
        bc = Blockchain()
        tp = TransactionPool()
        
        alice = Wallet()
        book = Book("123", "My Book", "Alice", alice.public_key_string())
        
        tx = alice.create_transaction(alice.public_key_string(), 0, "REGISTRATION", data=book.to_json())
        tp.add_transaction(tx)
        
        covered_txs = bc.get_covered_transaction_set(tp.transactions)
        assert len(covered_txs) == 1
        
        validator = Wallet()
        last_hash = BlockchainUtils.hash(bc.blocks[-1].payload()).hex()
        block = validator.create_block(covered_txs, last_hash, bc.blocks[-1].block_height + 1)
        bc.add_block(block)
        
        assert bc.asset_model.get_asset_owner("123") == alice.public_key_string()

    def test_asset_transfer(self):
        bc = Blockchain()
        tp = TransactionPool()
        
        alice = Wallet()
        bob = Wallet()
        
        book = Book("456", "Transfer Book", "Alice", alice.public_key_string())
        reg_tx = alice.create_transaction(alice.public_key_string(), 0, "REGISTRATION", data=book.to_json())
        
        bc.execute_transaction(reg_tx)
        assert bc.asset_model.get_asset_owner("456") == alice.public_key_string()
        
        book.owner_public_key = bob.public_key_string()
        transfer_tx = alice.create_transaction(bob.public_key_string(), 0, "TRANSFER", data=book.to_json())
        tp.add_transaction(transfer_tx)
        
        assert bc.transaction_covered(transfer_tx)
        
        bc.execute_transaction(transfer_tx)
        
        assert bc.asset_model.get_asset_owner("456") == bob.public_key_string()

    def test_invalid_transfer(self):
        bc = Blockchain()
        alice = Wallet()
        bob = Wallet()
        eve = Wallet()
        
        book = Book("789", "Secure Book", "Alice", alice.public_key_string())
        reg_tx = alice.create_transaction(alice.public_key_string(), 0, "REGISTRATION", data=book.to_json())
        bc.execute_transaction(reg_tx)
        
        book.owner_public_key = eve.public_key_string()
        theft_tx = eve.create_transaction(eve.public_key_string(), 0, "TRANSFER", data=book.to_json())
        
        assert not bc.transaction_covered(theft_tx)
