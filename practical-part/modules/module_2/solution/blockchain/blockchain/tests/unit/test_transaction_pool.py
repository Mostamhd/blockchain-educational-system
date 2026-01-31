from blockchain.transaction.transaction_pool import TransactionPool


class TestPoolOps:
    def test_inclusion(self, transaction):
        p = TransactionPool()
        assert not p.transaction_exists(transaction)
        p.add_transaction(transaction)
        assert p.transaction_exists(transaction)
