from blockchain.pos.proof_of_stake import ProofOfStake


class TestConsensus:
    def test_genesis_config(self):
        cp = ProofOfStake()
        assert cp.stakers
        assert len(cp.stakers) == 1

    def test_stake_modifications(self):
        cp = ProofOfStake()
        cp.update("a", 10)
        cp.update("b", 100)

        assert cp.get("a") == 10
        assert cp.get("b") == 100
        assert cp.get("c") is None

        cp.update("a", 5)
        assert cp.get("a") == 15

    def test_lot_allocation(self):
        cp = ProofOfStake()
        cp.update("a", 2)
        pool = cp.validator_lots("seed")
        
        a_lots = [l for l in pool if l.public_key == "a"]
        assert len(a_lots) == 2

    def test_selection_output(self):
        cp = ProofOfStake()
        cp.update("a", 10)
        
        winner = cp.forger("seed")
        assert isinstance(winner, str)
        assert winner in cp.stakers.keys()