from blockchain.blockchain import Blockchain
from blockchain.utils.helpers import BlockchainUtils
from blockchain.transaction.wallet import Wallet


class TestBlockchainCore:
    def test_append_new_block(self, transaction_pool):
        creator_wallet = transaction_pool["transaction_from_wallet"]["wallet"]
        tx_store = transaction_pool["pool"]

        new_block = creator_wallet.create_block(tx_store.transactions, "last_hash", 1)

        main_chain = Blockchain()
        main_chain.add_block(new_block)

        chain_data = main_chain.to_dict()

        assert len(chain_data["blocks"]) == 2
        assert chain_data["blocks"][0]["last_hash"] == "genesis_block"

    def test_chain_validation_logic(self, transaction_pool):
        creator_wallet = transaction_pool["transaction_from_wallet"]["wallet"]
        tx_store = transaction_pool["pool"]

        main_chain = Blockchain()

        latest_hash = BlockchainUtils.hash(main_chain.blocks[-1].payload()).hex()
        expected_height = main_chain.blocks[-1].block_height + 1
        
        valid_block = creator_wallet.create_block(tx_store.transactions, latest_hash, expected_height)
        assert main_chain.last_block_hash_valid(valid_block)
        assert main_chain.block_count_valid(valid_block)

        invalid_block = creator_wallet.create_block(tx_store.transactions, latest_hash, expected_height + 10)
        assert not main_chain.block_count_valid(invalid_block)

        main_chain.add_block(valid_block)
        
        chain_data = main_chain.to_dict()
        assert chain_data["blocks"]
        assert chain_data["blocks"][0]["last_hash"] == "genesis_block"

    def test_transaction_inclusion_verification(self):
        main_chain = Blockchain()
        alice = Wallet()
        bob = Wallet()
        
        tx = alice.create_transaction(bob.public_key_string(), 5, "TRANSFER")
        
        assert not main_chain.transaction_exists(tx)
        
        miner = Wallet()
        latest_hash = BlockchainUtils.hash(main_chain.blocks[-1].payload()).hex()
        new_block = miner.create_block([tx], latest_hash, 1)
        
        main_chain.add_block(new_block)
        
        assert main_chain.transaction_exists(tx)