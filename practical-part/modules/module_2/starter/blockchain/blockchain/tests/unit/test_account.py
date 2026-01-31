import pytest
from blockchain.blockchain import Blockchain
from blockchain.transaction.account_model import AccountModel
from blockchain.transaction.transaction_pool import TransactionPool
from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils


class TestAccountBalances:
    def test_update_workflow(self):
        w = Wallet()
        addr = w.public_key_string()
        am = AccountModel()

        am.add_account(addr)
        assert am.balances[addr] == 0
        
        am.update_balance(addr, 5)
        assert am.balances[addr] == 5

    def test_chain_state_persistence(self):
        bc = Blockchain()
        tp = TransactionPool()

        u1 = Wallet()
        u2 = Wallet()
        src = Wallet()
        v = Wallet()

        tx1 = src.create_transaction(
            u1.public_key_string(), 10, "EXCHANGE"
        )
        tp.add_transaction(tx1)

        txs = bc.get_covered_transaction_set(tp.transactions)
        h0 = BlockchainUtils.hash(bc.blocks[-1].payload()).hex()
        idx = bc.blocks[-1].block_height + 1
        
        b1 = v.create_block(txs, h0, idx)
        bc.add_block(b1)
        tp.remove_from_pool(b1.transactions)

        tx2 = u1.create_transaction(u2.public_key_string(), 5, "TRANSFER")
        tp.add_transaction(tx2)

        txs2 = bc.get_covered_transaction_set(tp.transactions)
        h1 = BlockchainUtils.hash(bc.blocks[-1].payload()).hex()
        idx2 = bc.blocks[-1].block_height + 1
        
        b2 = v.create_block(txs2, h1, idx2)
        bc.add_block(b2)
        
        snap = bc.to_dict()

        assert snap["blocks"][0]["last_hash"] == "genesis_block"
        assert snap["blocks"][1]["transactions"][0]["amount"] == 10
        assert snap["blocks"][2]["transactions"][0]["amount"] == 5
