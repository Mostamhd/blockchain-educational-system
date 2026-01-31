import pytest
from blockchain.blockchain import Blockchain
from blockchain.transaction.account_model import AccountModel
from blockchain.transaction.transaction_pool import TransactionPool
from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils


class TestLedgerAccounts:
    def test_balance_update_logic(self):
        inst = Wallet()
        key = inst.public_key_string()
        am = AccountModel()

        am.add_account(key)
        assert am.balances[key] == 0
        
        am.update_balance(key, 5)
        assert am.balances[key] == 5

    def test_state_changes_on_chain(self):
        bc = Blockchain()
        tp = TransactionPool()

        p1 = Wallet()
        p2 = Wallet()
        src = Wallet()
        v = Wallet()

        tx1 = src.create_transaction(
            p1.public_key_string(), 10, "EXCHANGE"
        )
        tp.add_transaction(tx1)

        set1 = bc.get_covered_transaction_set(tp.transactions)
        h0 = BlockchainUtils.hash(bc.blocks[-1].payload()).hex()
        idx = bc.blocks[-1].block_height + 1
        
        blk1 = v.create_block(set1, h0, idx)
        bc.add_block(blk1)
        tp.remove_from_pool(blk1.transactions)

        tx2 = p1.create_transaction(p2.public_key_string(), 5, "TRANSFER")
        tp.add_transaction(tx2)

        set2 = bc.get_covered_transaction_set(tp.transactions)
        h1 = BlockchainUtils.hash(bc.blocks[-1].payload()).hex()
        idx2 = bc.blocks[-1].block_height + 1
        
        blk2 = v.create_block(set2, h1, idx2)
        bc.add_block(blk2)
        
        dat = bc.to_dict()

        assert dat["blocks"][0]["last_hash"] == "genesis_group_05"
        assert dat["blocks"][1]["transactions"][0]["amount"] == 10
        assert dat["blocks"][2]["transactions"][0]["amount"] == 5
