class TestTxProperties:
    def test_schema(self, transaction):
        m = transaction.to_dict()

        assert m["id"]
        assert m["timestamp"]
        assert m["amount"] == 1
        assert m["type"] == "transfer"

    def test_auth_signature(self, transaction, wallet_signature):
        transaction.sign(wallet_signature)
        m = transaction.to_dict()

        assert m["id"]
        assert m["timestamp"]
        assert m["signature"] != ""
