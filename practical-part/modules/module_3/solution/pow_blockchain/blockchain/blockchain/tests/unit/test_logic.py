from blockchain.blockchain import Blockchain
from blockchain.transaction.wallet import Wallet
from blockchain.transaction.transaction_pool import TransactionPool
from blockchain.utils.helpers import BlockchainUtils


class TestRulesEngine:
    def test_balance_check(self):
        c = Blockchain()
        p = TransactionPool()
        
        u1 = Wallet()
        u2 = Wallet()
        
        t = u1.create_transaction(u2.public_key_string(), 10, "TRANSFER")
        p.add_transaction(t)
        
        set_tx = c.get_covered_transaction_set(p.transactions)
        
        assert len(set_tx) == 0
        assert not c.transaction_covered(t)

    def test_duplication_check(self):
        c = Blockchain()
        u1 = Wallet()
        m = Wallet()
        
        tx = m.create_transaction(u1.public_key_string(), 10, "EXCHANGE")
        
        lh = BlockchainUtils.hash(c.blocks[-1].payload()).hex()
        
        b = m.create_block([tx], lh, 1)
        c.add_block(b)
        
        assert c.transaction_exists(tx)
        assert c.transaction_exists(tx)
