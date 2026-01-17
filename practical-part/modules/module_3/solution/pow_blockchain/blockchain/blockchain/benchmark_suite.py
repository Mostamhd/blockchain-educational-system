import time
import requests
import threading
import json
import random
import pandas as pd
import matplotlib.pyplot as plt
from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils

# CONFIG
API_URL = "http://localhost:8050"  # Point to Node 1
TOTAL_TX = 500                     # Total transactions to send
TX_RATE = 20                       # Transactions per second (submission rate)
OUTPUT_FILE = "benchmark_results.csv"

def send_transaction(wallet):
    """Creates and sends a single transaction"""
    tx = wallet.create_transaction(wallet.public_key_string(), 1, "EXCHANGE")
    payload = {"transaction": BlockchainUtils.encode(tx)}
    try:
        requests.post(f"{API_URL}/api/v1/transaction/create/", json=payload, timeout=0.5)
    except:
        pass

def load_generator(wallet, stop_event):
    """Spams transactions at a specific rate"""
    while not stop_event.is_set():
        # Send a burst
        start = time.time()
        send_transaction(wallet)
        elapsed = time.time() - start
        
        # Sleep to maintain rate
        sleep_time = (1.0 / TX_RATE) - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

def get_chain_stats():
    """Fetches chain data to calculate TPS"""
    try:
        res = requests.get(f"{API_URL}/api/v1/blockchain/")
        chain = res.json()['blocks']
        return chain
    except:
        return []

def run_benchmark(mode_name="POW"):
    print(f"--- Starting Benchmark: {mode_name} ---")
    wallet = Wallet()
    stop_event = threading.Event()
    
    # 1. Start Load Generator
    print("Generating Load...")
    gen_thread = threading.Thread(target=load_generator, args=(wallet, stop_event))
    gen_thread.start()
    
    # 2. Monitor Confirmation
    start_time = time.time()
    initial_block_height = len(get_chain_stats())
    confirmed_tx = 0
    
    # Run for a fixed duration (e.g., 60 seconds)
    DURATION = 60
    time.sleep(DURATION)
    
    stop_event.set()
    gen_thread.join()
    
    # 3. Wait a bit for pending blocks
    print("Waiting for final blocks...")
    time.sleep(10) 
    
    # 4. Analyze
    chain = get_chain_stats()
    end_time = time.time()
    
    # Calculate Metrics
    tx_count = 0
    propagation_delays = []
    
    for block in chain:
        if block['block_height'] >= initial_block_height:
            # Count transactions (exclude Coinbase)
            tx_count += max(0, len(block['transactions']) - 1)
            
            # Note: Propagation delay must be parsed from Docker logs, 
            # but we can estimate block time here.
            
    tps = tx_count / (end_time - start_time)
    
    print(f"--- Results ({mode_name}) ---")
    print(f"Total TX Confirmed: {tx_count}")
    print(f"Time Elapsed: {end_time - start_time:.2f}s")
    print(f"TPS: {tps:.2f}")
    
    return {
        "mode": mode_name,
        "tps": tps,
        "total_tx": tx_count
    }

if __name__ == "__main__":
    # You would run this once for PoS, save data, restart docker with PoW, run again.
    # For now, let's assume we are running the current mode.
    data = run_benchmark("CURRENT_MODE")
    
    # Save to file
    df = pd.DataFrame([data])
    df.to_csv(OUTPUT_FILE, mode='a', header=False)
