from blockchain.transaction.transaction_pool import TransactionPool


class TestMempool:
    def test_pool_ingestion(self, transaction):
        mempool = TransactionPool()
        assert not mempool.transaction_exists(transaction)
        mempool.add_transaction(transaction)
        assert mempool.transaction_exists(transaction)