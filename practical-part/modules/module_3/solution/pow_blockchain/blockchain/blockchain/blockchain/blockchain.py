import logging
import copy
import time

from blockchain.block import Block
from blockchain.pow.proof_of_work import ProofOfWork
from blockchain.transaction.account_model import AccountModel
from blockchain.utils.helpers import BlockchainUtils
from blockchain.utils.logger import logger


class Blockchain:
    def __init__(self):
        self.blocks = [Block.genesis()]
        self.account_model = AccountModel()
        self.pow = ProofOfWork()
        self.peers = None
        
        self.block_time = 10
        self.block_reward = 10
        self.difficulty = 4.0
        self.difficulty_adjustment_interval = 5
        self.max_block_size = 102400 

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
        sender_balance = self.account_model.get_balance(transaction.sender_public_key)
        if sender_balance >= transaction.amount:
            return True
        return False

    def execute_transactions(self, transactions):
        for transaction in transactions:
            self.execute_transaction(transaction)

    def execute_transaction(self, transaction):
        sender = transaction.sender_public_key
        receiver = transaction.receiver_public_key
        amount = transaction.amount
        self.account_model.update_balance(sender, -amount)
        self.account_model.update_balance(receiver, amount)
        
    def adjust_difficulty(self):
        if len(self.blocks) % self.difficulty_adjustment_interval == 0 and len(self.blocks) > 0:
            
            prev_adjustment_block = self.blocks[-self.difficulty_adjustment_interval]
            last_block = self.blocks[-1]
            
            time_taken = last_block.timestamp - prev_adjustment_block.timestamp
            expected_time = self.block_time * self.difficulty_adjustment_interval
            
            logger.info({"message":f"DEBUG: Time Taken: {time_taken:.2f}s | Expected: {expected_time}s"})

            if time_taken < expected_time:
                self.difficulty += 0.1
                logger.info({"message":f"DEBUG: Too Fast! Difficulty increased to {self.difficulty:.2f}"})
                
            elif time_taken > expected_time:
                self.difficulty -= 0.1
                if self.difficulty < 1.0:
                    self.difficulty = 1.0
                logger.info(f"DEBUG: Too Slow! Difficulty decreased to {self.difficulty:.2f}")
        
        return self.difficulty

    def create_block(self, transactions_from_pool, forger_wallet, abort_event=None):
        covered_transactions = self.get_covered_transaction_set(transactions_from_pool)
        
        selected_transactions = []
        current_block_size = 0
        for transaction in covered_transactions:
            tx_string = BlockchainUtils.encode(transaction)
            tx_size = len(tx_string)
            if current_block_size + tx_size > self.max_block_size:
                break
            selected_transactions.append(transaction)
            current_block_size += tx_size
        
        self.execute_transactions(selected_transactions)
        
        current_difficulty = self.adjust_difficulty()

        new_block = forger_wallet.create_block(
            selected_transactions,
            BlockchainUtils.hash(self.blocks[-1].payload()).hex(),
            len(self.blocks)
        )
        
        new_block.difficulty = current_difficulty

        mined_block = self.pow.mine(new_block, current_difficulty, abort_event)
        
        if mined_block:
            self.blocks.append(mined_block)
            
        return mined_block

    def transaction_exists(self, transaction):
        for block in self.blocks:
            for block_transaction in block.transactions:
                if transaction.equals(block_transaction):
                    return True
        return False
    
    def get_transaction(self, transaction_hash):
        for block in self.blocks:
            for block_transaction in block.transactions:
                if block_transaction.signature == transaction_hash:
                    return block_transaction
        return False

    def proof_valid(self, block):
        return self.pow.validate(block, block.difficulty)

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