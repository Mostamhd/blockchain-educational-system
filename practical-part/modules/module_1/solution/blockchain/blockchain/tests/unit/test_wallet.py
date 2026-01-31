from blockchain.transaction.wallet import Wallet


class TestKeyWallet:
    def test_signature_validation(self, transaction):
        w = Wallet()
        s = w.sign(transaction.payload())
        
        assert Wallet.signature_valid(transaction.payload(), s, w.public_key_string())
        assert not Wallet.signature_valid({"a": "b"}, s, w.public_key_string())

    def test_address_prefix(self):
        w = Wallet()
        assert "0x" in w.public_key_string()

    def test_transaction_creation(self):
        w1 = Wallet()
        w2 = Wallet()
        tx = w1.create_transaction(w2.public_key_string(), 10, "TRANSFER")
        
        assert tx.sender_public_key == w1.public_key_string()
        assert tx.receiver_public_key == w2.public_key_string()
        assert tx.amount == 10
        assert tx.signature != ""
        
    def test_block_creation(self, transaction_pool):
        w = transaction_pool["transaction_from_wallet"]["wallet"]
        p = transaction_pool["pool"]
        
        b = w.create_block(p.transactions, "prev", 1)
        assert b.forger == w.public_key_string()
        assert b.signature != ""
        assert b.transactions == p.transactions
