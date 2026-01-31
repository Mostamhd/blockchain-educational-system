from eth_keys import keys
from eth_utils import encode_hex, keccak
import secrets

private_key_bytes = secrets.token_bytes(32)
private_key = keys.PrivateKey(private_key_bytes)
public_key = private_key.public_key

private_key_hex = encode_hex(private_key.to_bytes())
public_key_hex = encode_hex(public_key.to_bytes())

eth_address = encode_hex(keccak(public_key.to_bytes())[-20:])

with open("staker_private_key.txt", "w") as key_file:
    key_file.write(private_key_hex)

with open("staker_eth_address.txt", "w") as key_file:
    key_file.write(eth_address)
    
with open("staker_public_key.txt", "w") as key_file:
    key_file.write(public_key_hex)

print("Private key:", private_key_hex)
print("Public key:", public_key_hex)
print("Ethereum address:", eth_address)