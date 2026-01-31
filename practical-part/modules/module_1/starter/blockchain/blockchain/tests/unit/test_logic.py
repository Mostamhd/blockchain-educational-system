from blockchain.blockchain import Blockchain
from blockchain.transaction.wallet import Wallet
from blockchain.transaction.transaction_pool import TransactionPool
from blockchain.utils.helpers import BlockchainUtils


class TestBlockchainLogic:
    def test_insufficient_balance_transaction(self):
        blockchain = Blockchain()
        pool = TransactionPool()
        
        alice = Wallet()
        bob = Wallet()
        
        invalid_tx = alice.create_transaction(bob.public_key_string(), 10, "TRANSFER")
        pool.add_transaction(invalid_tx)
        
        covered_transactions = blockchain.get_covered_transaction_set(pool.transactions)
        
        assert len(covered_transactions) == 0
        assert not blockchain.transaction_covered(invalid_tx)

    def test_transaction_replay_prevention_logic(self):
        blockchain = Blockchain()
        alice = Wallet()
        miner = Wallet()
        
        exchange_tx = miner.create_transaction(alice.public_key_string(), 10, "EXCHANGE")
        
        latest_hash = BlockchainUtils.hash(blockchain.blocks[-1].payload()).hex()
        
        block = miner.create_block([exchange_tx], latest_hash, 1)
        blockchain.add_block(block)
        
        assert blockchain.transaction_exists(exchange_tx)
        
        assert blockchain.transaction_exists(exchange_tx)