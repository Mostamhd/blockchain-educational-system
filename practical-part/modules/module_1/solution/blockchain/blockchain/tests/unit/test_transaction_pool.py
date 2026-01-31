from blockchain.transaction.transaction_pool import TransactionPool


class TestPool:
    def test_item_management(self, transaction):
        inst = TransactionPool()
        assert not inst.transaction_exists(transaction)
        inst.add_transaction(transaction)
        assert inst.transaction_exists(transaction)
