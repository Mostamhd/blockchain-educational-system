from blockchain.pos.proof_of_stake import ProofOfStake


class TestPoSConsensus:
    def test_startup_stakers(self):
        obj = ProofOfStake()
        assert obj.stakers
        assert len(obj.stakers) == 1

    def test_registry_modifications(self):
        obj = ProofOfStake()
        obj.update("x", 10)
        obj.update("y", 100)

        assert obj.get("x") == 10
        assert obj.get("y") == 100
        assert obj.get("z") is None

        obj.update("x", 5)
        assert obj.get("x") == 15

    def test_lot_generation_integrity(self):
        obj = ProofOfStake()
        obj.update("x", 2)
        lots = obj.validator_lots("seed")
        
        x_lots = [i for i in lots if i.public_key == "x"]
        assert len(x_lots) == 2

    def test_forger_output_type(self):
        obj = ProofOfStake()
        obj.update("x", 10)
        
        winner = obj.forger("seed")
        assert isinstance(winner, str)
        assert winner in obj.stakers.keys()