import time
import copy
import threading

from api.main import NodeAPI
from blockchain.blockchain import Blockchain
from blockchain.p2p.message import Message
from blockchain.p2p.socket_communication import SocketCommunication
from blockchain.transaction.transaction_pool import TransactionPool
from blockchain.transaction.transaction import Transaction
from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils
from blockchain.utils.logger import logger


class Node:
    def __init__(self, ip, port, api_port, key=None):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.api_port = api_port
        self.transaction_pool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()
        
        if key:
            self.wallet.from_key(key)
            
        self.abort_mining = threading.Event()
        
        self.keep_running = True
        self.start_p2p()
        self.start_node_api()
        self.start_produce_block()

    def start_p2p(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.start_socket_communication(self)

    def start_node_api(self):
        self.api = NodeAPI()
        self.api.inject_node(self)
        api_thread = threading.Thread(target=self.api.start, args=(self.ip, self.api_port))
        api_thread.daemon = True
        api_thread.start()

    def start_produce_block(self):
        produce_thread = threading.Thread(target=self.run_produce_block)
        produce_thread.daemon = True
        produce_thread.start()

    def run_produce_block(self):
        while self.keep_running:
            self.produce_block()
            time.sleep(1)

    def stop(self):
        self.keep_running = False

    def produce_block(self):
        self.create_coinbase_transaction()
        
        self.abort_mining.clear()
        
        block = self.blockchain.create_block(
            self.transaction_pool.transactions, 
            self.wallet, 
            self.abort_mining
        )
        
        if block:
            self.transaction_pool.remove_from_pool(block.transactions)
            message = Message(self.p2p.socket_connector, "BLOCK", block)
            self.p2p.broadcast(BlockchainUtils.encode(message))
        else:
            pass

    def create_coinbase_transaction(self):
        transaction = self.wallet.create_coinbase_transaction(
            self.wallet.public_key_string(), 
            self.blockchain.block_reward, 
            'COINBASE'
        )
        self.transaction_pool.add_transaction(transaction)

    def handle_transaction(self, transaction):
        data = transaction.payload()
        signature = transaction.signature
        signer_public_key = transaction.sender_public_key
        signature_valid = Wallet.signature_valid(data, signature, signer_public_key)
        transaction_exists = self.transaction_pool.transaction_exists(transaction)
        transaction_in_block = self.blockchain.transaction_exists(transaction)

        if not transaction_exists and not transaction_in_block and signature_valid:
            self.transaction_pool.add_transaction(transaction)
            message = Message(self.p2p.socket_connector, "TRANSACTION", transaction)
            self.p2p.broadcast(BlockchainUtils.encode(message))

    def handle_block(self, block):
        block_hash = block.payload()
        signature = block.signature

        block_count_valid = self.blockchain.block_count_valid(block)
        last_block_hash_valid = self.blockchain.last_block_hash_valid(block)
        transactions_valid = self.blockchain.transactions_valid(block.transactions)
        
        proof_valid = self.blockchain.proof_valid(block)
        
        signature_valid = Wallet.signature_valid(block_hash, signature, block.forger)

        if not block_count_valid:
            self.request_chain()

        if (
            last_block_hash_valid
            and proof_valid
            and transactions_valid
            and signature_valid
        ):
            self.blockchain.add_block(block)
            
            self.abort_mining.set()
            
            self.transaction_pool.remove_from_pool(block.transactions)
            message = Message(self.p2p.socket_connector, "BLOCK", block)
            self.p2p.broadcast(BlockchainUtils.encode(message))

    def request_chain(self):
        message = Message(self.p2p.socket_connector, "BLOCKCHAINREQUEST", None)
        encoded_message = BlockchainUtils.encode(message)
        self.p2p.broadcast(encoded_message)

    def handle_blockchain_request(self, requesting_node):
        message = Message(self.p2p.socket_connector, "BLOCKCHAIN", self.blockchain)
        encoded_message = BlockchainUtils.encode(message)
        self.p2p.send(requesting_node, encoded_message)

    def handle_blockchain_v1(self, blockchain):
        local_blockchain_copy = copy.deepcopy(self.blockchain)
        local_block_count = len(local_blockchain_copy.blocks)
        received_chain_block_count = len(blockchain.blocks)
        if local_block_count < received_chain_block_count:
            for block_number, block in enumerate(blockchain.blocks):
                if block_number >= local_block_count:
                    local_blockchain_copy.add_block(block)
                    self.transaction_pool.remove_from_pool(block.transactions)
            self.blockchain = local_blockchain_copy

    def handle_blockchain(self, blockchain):
        local_blockchain_copy = copy.deepcopy(self.blockchain)
        local_block_count = len(local_blockchain_copy.blocks)
        received_chain_block_count = len(blockchain.blocks)

        if received_chain_block_count > local_block_count:
            
            lost_transactions = [] 
            self.blockchain = blockchain
            
            for block in self.blockchain.blocks:
                self.transaction_pool.remove_from_pool(block.transactions)
            for tx in lost_transactions:
                if not self.blockchain.transaction_exists(tx):
                    self.transaction_pool.add_transaction(tx)