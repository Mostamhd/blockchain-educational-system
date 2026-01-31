import requests

from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils


def post_transaction(sender, receiver, amount, type):
    transaction = sender.create_transaction(receiver.public_key_string(), amount, type)
    url = "http://localhost:8050/api/v1/transaction/create/"
    package = {"transaction": BlockchainUtils.encode(transaction)}
    response = requests.post(url, json=package, timeout=15)
    print(response.text)


if __name__ == "__main__":
    john = Wallet()
    jane = Wallet()
    jane.from_key("/blockchain/keys/genesis_private_key.txt")
    john.from_key("/blockchain/keys/staker_private_key.txt")

    exchange = Wallet()

    post_transaction(exchange, jane, 100, "EXCHANGE")
    post_transaction(exchange, john, 100, "EXCHANGE")
    post_transaction(exchange, john, 10, "EXCHANGE")
    post_transaction(john, john, 100, "STAKE")

    post_transaction(jane, john, 1, "TRANSFER")
    post_transaction(jane, john, 1, "TRANSFER")

    post_transaction(jane, john, 1, "TRANSFER")