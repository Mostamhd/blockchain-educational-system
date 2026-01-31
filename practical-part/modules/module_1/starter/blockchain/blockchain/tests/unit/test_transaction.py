class TestTransactionModel:
    def test_default_properties(self, transaction):
        data_map = transaction.to_dict()

        assert data_map["id"]
        assert data_map["timestamp"]
        assert data_map["amount"] == 1
        assert data_map["type"] == "transfer"

    def test_signing_process(self, transaction, wallet_signature):
        transaction.sign(wallet_signature)
        data_map = transaction.to_dict()

        assert data_map["id"]
        assert data_map["timestamp"]
        assert data_map["signature"] != ""