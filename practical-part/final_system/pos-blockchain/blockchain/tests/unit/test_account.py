import pytest
from blockchain.blockchain import Blockchain
from blockchain.transaction.account_model import AccountModel
from blockchain.transaction.transaction_pool import TransactionPool
from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils


class TestAccountSystem:
    def test_balance_updates_correctly(self):
        user_wallet = Wallet()
        user_pub_key = user_wallet.public_key_string()
        accounts = AccountModel()

        accounts.add_account(user_pub_key)
        assert accounts.balances[user_pub_key] == 0
        
        accounts.update_balance(user_pub_key, 5)
        assert accounts.balances[user_pub_key] == 5

    def test_ledger_state_updates(self):
        chain_instance = Blockchain()
        mempool = TransactionPool()

        alice = Wallet()
        bob = Wallet()
        bank = Wallet()
        validator = Wallet()

        funding_tx = bank.create_transaction(
            alice.public_key_string(), 10, "EXCHANGE"
        )
        mempool.add_transaction(funding_tx)

        pending_txs = chain_instance.get_covered_transaction_set(mempool.transactions)
        prev_hash = BlockchainUtils.hash(chain_instance.blocks[-1].payload()).hex()
        next_height = chain_instance.blocks[-1].block_height + 1
        
        first_block = validator.create_block(pending_txs, prev_hash, next_height)
        chain_instance.add_block(first_block)
        mempool.remove_from_pool(first_block.transactions)

        transfer_tx = alice.create_transaction(bob.public_key_string(), 5, "TRANSFER")
        mempool.add_transaction(transfer_tx)

        pending_txs_2 = chain_instance.get_covered_transaction_set(mempool.transactions)
        prev_hash_2 = BlockchainUtils.hash(chain_instance.blocks[-1].payload()).hex()
        next_height_2 = chain_instance.blocks[-1].block_height + 1
        
        second_block = validator.create_block(pending_txs_2, prev_hash_2, next_height_2)
        chain_instance.add_block(second_block)
        
        ledger_snapshot = chain_instance.to_dict()

        assert ledger_snapshot["blocks"][0]["last_hash"] == "genesis_block"
        assert ledger_snapshot["blocks"][1]["transactions"][0]["amount"] == 10
        assert ledger_snapshot["blocks"][2]["transactions"][0]["amount"] == 5