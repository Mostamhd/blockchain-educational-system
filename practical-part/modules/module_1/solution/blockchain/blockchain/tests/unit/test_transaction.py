class TestTxData:
    def test_field_presence(self, transaction):
        dat = transaction.to_dict()

        assert dat["id"]
        assert dat["timestamp"]
        assert dat["amount"] == 1
        assert dat["type"] == "transfer"

    def test_signature_attachment(self, transaction, wallet_signature):
        transaction.sign(wallet_signature)
        dat = transaction.to_dict()

        assert dat["id"]
        assert dat["timestamp"]
        assert dat["signature"] != ""
