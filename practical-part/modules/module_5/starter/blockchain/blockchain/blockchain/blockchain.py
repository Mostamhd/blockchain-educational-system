import logging
import json

from blockchain.block import Block
from blockchain.pos.proof_of_stake import ProofOfStake
from blockchain.transaction.account_model import AccountModel
from blockchain.transaction.asset_model import AssetModel
from blockchain.utils.helpers import BlockchainUtils


class Blockchain:
    def __init__(self):
        self.blocks = [Block.genesis()]
        self.account_model = AccountModel()
        self.asset_model = AssetModel()
        self.pos = ProofOfStake()
        self.block_time = 10
        self.block_reward = 10
        self.peers = None

    def get_block_by_height(self, block_height):
        for block in self.blocks:
            if block.block_height == block_height:
                return block
        return None

    def add_block(self, block):
        self.execute_transactions(block.transactions)
        self.blocks.append(block)

    def to_dict(self):
        data = {}
        blocks_readable = []
        for block in self.blocks:
            blocks_readable.append(block.to_dict())
        data["blocks"] = blocks_readable
        return data

    def block_count_valid(self, block):
        if self.blocks[-1].block_height == block.block_height - 1:
            return True
        return False

    def last_block_hash_valid(self, block):
        last_block_chain_block_hash = BlockchainUtils.hash(
            self.blocks[-1].payload()
        ).hex()
        if last_block_chain_block_hash == block.last_hash:
            return True
        return False

    def get_covered_transaction_set(self, transactions):
        covered_transactions = []
        for transaction in transactions:
            if self.transaction_covered(transaction):
                covered_transactions.append(transaction)
            else:
                logging.error("Transaction is not covered by sender")
        return covered_transactions

    def transaction_covered(self, transaction):
        if transaction.type == "EXCHANGE" or transaction.type == "COINBASE":
            return True
        
        if transaction.type == "REGISTRATION":
            try:
                data = json.loads(transaction.data)
                isbn = data.get("isbn")
                if not isbn:
                    return False
                if self.asset_model.get_asset_owner(isbn):
                    logging.error(f"Registration failed: Asset {isbn} already exists.")
                    return False
                return True
            except Exception:
                logging.error("Registration failed: Invalid data format.")
                return False

        if transaction.type == "TRANSFER":
            try:
                data = json.loads(transaction.data)
                isbn = data.get("isbn")
                if not isbn:
                    return False
                current_owner = self.asset_model.get_asset_owner(isbn)
                if not current_owner:
                    logging.error(f"Transfer failed: Asset {isbn} not found.")
                    return False
                if current_owner != transaction.sender_public_key:
                    logging.error(f"Transfer failed: Sender {transaction.sender_public_key} is not the owner of {isbn}.")
                    return False
                return True
            except Exception:
                logging.error("Transfer failed: Invalid data format.")
                return False

        sender_balance = self.account_model.get_balance(transaction.sender_public_key)
        if sender_balance >= transaction.amount:
            return True
        return False

    def execute_transactions(self, transactions):
        for transaction in transactions:
            self.execute_transaction(transaction)

    def execute_transaction(self, transaction):
        if transaction.type == "STAKE":
            sender = transaction.sender_public_key
            receiver = transaction.receiver_public_key
            if sender == receiver:
                amount = transaction.amount
                self.pos.update(sender, amount)
                self.account_model.update_balance(sender, -amount)
        elif transaction.type == "REGISTRATION":
            try:
                data = json.loads(transaction.data)
                isbn = data.get("isbn")
                owner = data.get("owner_public_key")
                if isbn and owner:
                    self.asset_model.add_asset(isbn, owner)
            except Exception:
                pass
        elif transaction.type == "TRANSFER":
            try:
                data = json.loads(transaction.data)
                isbn = data.get("isbn")
                new_owner = data.get("owner_public_key")
                if isbn and new_owner:
                    self.asset_model.update_asset_owner(isbn, new_owner)
            except Exception:
                pass
        else:
            sender = transaction.sender_public_key
            receiver = transaction.receiver_public_key
            amount = transaction.amount
            self.account_model.update_balance(sender, -amount)
            self.account_model.update_balance(receiver, amount)

    def next_forger(self):
        last_block_hash = BlockchainUtils.hash(self.blocks[-1].payload()).hex()
        next_forger = self.pos.forger(last_block_hash)
        return next_forger

    def create_block(self, transactions_from_pool, forger_wallet):
        covered_transactions = self.get_covered_transaction_set(transactions_from_pool)
        self.execute_transactions(covered_transactions)
        new_block = forger_wallet.create_block(
            covered_transactions,
            BlockchainUtils.hash(self.blocks[-1].payload()).hex(),
            len(self.blocks),
        )
        self.blocks.append(new_block)
        return new_block

    def transaction_exists(self, transaction):
        for block in self.blocks:
            for block_transaction in block.transactions:
                if transaction.equals(block_transaction):
                    return True
        return False
    
    def get_transaction(self, transaction_signature):
        for block in self.blocks:
            for block_transaction in block.transactions:
                if block_transaction.signature == transaction_signature:
                    return block_transaction
        return False

    def forger_valid(self, block):
        forger_public_key = self.pos.forger(block.last_hash)
        proposed_block_forger = block.forger
        if forger_public_key == proposed_block_forger:
            return True
        return False

    def transactions_valid(self, transactions):
        covered_transactions = self.get_covered_transaction_set(transactions)
        if len(covered_transactions) == len(transactions):
            return True
        return False
    
    def get_address_balance(self, public_key):
        return self.account_model.get_balance(public_key)

    def get_address_transactions(self, public_key):
        transactions = []
        for block in self.blocks:
            for block_transaction in block.transactions:
                if block_transaction.sender_public_key == public_key or block_transaction.receiver_public_key == public_key:
                    transactions.append(block_transaction)
        return transactions