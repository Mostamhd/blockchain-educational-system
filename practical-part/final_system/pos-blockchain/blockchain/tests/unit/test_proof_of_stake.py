from blockchain.pos.proof_of_stake import ProofOfStake


class TestConsensusMechanism:
    def test_genesis_stake_exists(self):
        consensus = ProofOfStake()
        assert consensus.stakers
        assert len(consensus.stakers) == 1

    def test_stake_registry_updates(self):
        consensus = ProofOfStake()
        consensus.update("alice", 10)
        consensus.update("bob", 100)

        assert consensus.get("alice") == 10
        assert consensus.get("bob") == 100
        assert consensus.get("charlie") is None

        consensus.update("alice", 5)
        assert consensus.get("alice") == 15

    def test_lot_generation_count(self):
        consensus = ProofOfStake()
        consensus.update("alice", 2)
        lot_pool = consensus.validator_lots("seed")
        
        alice_lots = [item for item in lot_pool if item.public_key == "alice"]
        assert len(alice_lots) == 2

    def test_leader_election_integrity(self):
        consensus = ProofOfStake()
        consensus.update("alice", 10)
        
        elected_forger = consensus.forger("random_seed_string")
        assert isinstance(elected_forger, str)
        assert elected_forger in consensus.stakers.keys()
