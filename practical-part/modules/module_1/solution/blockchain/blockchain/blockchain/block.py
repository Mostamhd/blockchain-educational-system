import copy
import time
from blockchain.utils.helpers import BlockchainUtils 


class Block:
    def __init__(self, transactions, last_hash, forger, block_height):
        self.transactions = transactions
        self.last_hash = last_hash
        self.forger = forger
        self.block_height = block_height
        self.timestamp = time.time()
        self.signature = ""
        self.hash = ""
        
    @staticmethod
    def genesis():
        genesis_block = Block([], "genesis_group_05", "genesis", 0)
        genesis_block.timestamp = time.time()
        genesis_block.hash = BlockchainUtils.hash(genesis_block.payload()).hex()
        return genesis_block

    def to_dict(self):
        data = copy.deepcopy(self.__dict__)
        transactions_readable = []
        for transaction in data["transactions"]:
            transactions_readable.append(transaction.to_dict())
        data["transactions"] = transactions_readable
        return data

    def payload(self):
        dict_representation = copy.deepcopy(self.to_dict())
        dict_representation["signature"] = ""
        dict_representation["hash"] = ""
        return dict_representation

    def sign(self, signature):
        self.signature = signature
        self.hash = BlockchainUtils.hash(self.payload()).hex()