import copy
import time
import uuid
from blockchain.utils.helpers import BlockchainUtils

class Transaction:
    def __init__(self, sender_public_key, receiver_public_key, amount, type):
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key
        self.amount = amount
        self.type = type
        self.id = uuid.uuid1().hex
        self.timestamp = time.time()
        self.signature = ""
        self.hash = None

    def to_dict(self):
        return self.__dict__

    def sign(self, signature):
        self.signature = signature
        self.hash = BlockchainUtils.hash(self.payload()).hex()
          
    def payload(self):
        dict_representation = copy.deepcopy(self.to_dict())
        dict_representation["signature"] = ""
        dict_representation["hash"] = ""
        return dict_representation

    def equals(self, transaction):
        if self.id == transaction.id:
            return True
        return False
