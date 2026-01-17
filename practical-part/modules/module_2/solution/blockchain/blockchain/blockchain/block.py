import copy
import time


class Block:
    def __init__(self, transactions, last_hash, forger, block_height, nonce=0, difficulty=1):
        self.transactions = transactions
        self.last_hash = last_hash
        self.forger = forger
        self.block_height = block_height
        self.timestamp = time.time()
        self.signature = ""
        self.nonce = nonce
        self.difficulty = difficulty

    @staticmethod
    def genesis():
        # Genesis block with arbitrary nonce and difficulty
        genesis_block = Block([], "genesis_hash", "genesis", 0, 0, 1)
        genesis_block.timestamp = time.time()
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
        return dict_representation

    def sign(self, signature):
        self.signature = signature