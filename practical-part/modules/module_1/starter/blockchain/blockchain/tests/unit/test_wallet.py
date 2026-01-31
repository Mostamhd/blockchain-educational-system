from blockchain.transaction.wallet import Wallet


class TestWalletFunctionality:
    def test_crypto_signature_checks(self, transaction):
        user_wallet = Wallet()
        sig = user_wallet.sign(transaction.payload())
        
        assert Wallet.signature_valid(transaction.payload(), sig, user_wallet.public_key_string())
        
        assert not Wallet.signature_valid({"data": "garbage"}, sig, user_wallet.public_key_string())

    def test_key_format_standards(self):
        user_wallet = Wallet()
        assert "0x" in user_wallet.public_key_string()

    def test_tx_generation(self):
        sender_wallet = Wallet()
        receiver_wallet = Wallet()
        new_tx = sender_wallet.create_transaction(receiver_wallet.public_key_string(), 10, "TRANSFER")
        
        assert new_tx.sender_public_key == sender_wallet.public_key_string()
        assert new_tx.receiver_public_key == receiver_wallet.public_key_string()
        assert new_tx.amount == 10
        assert new_tx.signature != ""
        
    def test_block_minting(self, transaction_pool):
        minter_wallet = transaction_pool["transaction_from_wallet"]["wallet"]
        tx_source = transaction_pool["pool"]
        
        minted_block = minter_wallet.create_block(tx_source.transactions, "last_hash", 1)
        assert minted_block.forger == minter_wallet.public_key_string()
        assert minted_block.signature != ""
        assert minted_block.transactions == tx_source.transactions