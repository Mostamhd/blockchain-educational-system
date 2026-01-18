import sys
import os
import json
import urllib.request
import urllib.error

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from blockchain.transaction.wallet import Wallet
from blockchain.transaction.digital_asset import Book
from blockchain.utils.helpers import BlockchainUtils

def transfer_book():
    print("--- Transferring Book ---")

    wallet = Wallet()
    key_file = os.path.join(current_dir, 'keys/genesis_private_key.txt')
    if os.path.exists(key_file):
        wallet.from_key(key_file)
        print(f"Loaded owner wallet: {wallet.public_key_string()[:20]}...")
    else:
        print("Using new random wallet (might fail if original owner needed matches).")


    new_owner = Wallet()
    print(f"New owner wallet: {new_owner.public_key_string()[:20]}...")


    book = Book(
        isbn="978-3-16-148410-0",
        title="The Blockchain Thesis",
        author="Moustafa",
        owner_public_key=new_owner.public_key_string()
    )
    print(f"Book update prepared for ISBN: {book.isbn}")


    transaction = wallet.create_transaction(
        receiver=new_owner.public_key_string(),
        amount=0,
        type="TRANSFER",
        data=book.to_json()
    )


    payload = {"transaction": BlockchainUtils.encode(transaction)}
    data = json.dumps(payload).encode('utf-8')
    url = "http://localhost:8050/api/v1/transaction/create/"
    print(f"Sending transaction to {url}...")
    
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            resp_data = response.read().decode('utf-8')
            print(f"Response: {resp_data}")
            print(f"Transaction ID: {transaction.id}")
    except urllib.error.URLError as e:
        print(f"Error sending transaction: {e}")
        print("Ensure the node is running on localhost:8050")

if __name__ == "__main__":
    transfer_book()
