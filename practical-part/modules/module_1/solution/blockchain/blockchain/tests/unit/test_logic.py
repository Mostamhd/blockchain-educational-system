from blockchain.blockchain import Blockchain
from blockchain.transaction.wallet import Wallet
from blockchain.transaction.transaction_pool import TransactionPool
from blockchain.utils.helpers import BlockchainUtils


class TestBusinessLogic:
    def test_overdraft_prevention(self):
        inst = Blockchain()
        pool = TransactionPool()
        
        u1 = Wallet()
        u2 = Wallet()
        
        tx = u1.create_transaction(u2.public_key_string(), 10, "TRANSFER")
        pool.add_transaction(tx)
        
        valid_txs = inst.get_covered_transaction_set(pool.transactions)
        
        assert len(valid_txs) == 0
        assert not inst.transaction_covered(tx)

    def test_history_duplication(self):
        inst = Blockchain()
        u1 = Wallet()
        m = Wallet()
        
        tx = m.create_transaction(u1.public_key_string(), 10, "EXCHANGE")
        
        lh = BlockchainUtils.hash(inst.blocks[-1].payload()).hex()
        
        b = m.create_block([tx], lh, 1)
        inst.add_block(b)
        
        assert inst.transaction_exists(tx)
        assert inst.transaction_exists(tx)
