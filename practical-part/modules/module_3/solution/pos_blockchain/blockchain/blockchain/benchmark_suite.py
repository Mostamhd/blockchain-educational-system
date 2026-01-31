import time
import requests
import threading
import pandas as pd
from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils

class BenchmarkSuite:
    def __init__(self, api_url="http://localhost:8050", tx_rate=20, duration=60, output_file="benchmark_results.csv"):
        self.api_url = api_url
        self.tx_rate = tx_rate
        self.duration = duration
        self.output_file = output_file
        self.wallet = Wallet()
        self.stop_event = threading.Event()

    def wait_for_api(self):
        print(f"Benchmark: Waiting for API at {self.api_url}...")
        while not self.stop_event.is_set():
            try:
                requests.get(f"{self.api_url}/api/v1/blockchain/", timeout=1)
                print("Benchmark: API is online.")
                return True
            except:
                time.sleep(1)
        return False

    def send_transaction(self):
        tx = self.wallet.create_transaction(self.wallet.public_key_string(), 1, "EXCHANGE")
        payload = {"transaction": BlockchainUtils.encode(tx)}
        try:
            requests.post(f"{self.api_url}/api/v1/transaction/create/", json=payload, timeout=2)
        except Exception as e:
            print(f"TX Submission Failed: {e}")

    def load_generator(self):
        print("Benchmark: Starting load generation...")
        while not self.stop_event.is_set():
            start = time.time()
            self.send_transaction()
            elapsed = time.time() - start
            sleep_time = (1.0 / self.tx_rate) - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    def get_chain_stats(self):
        try:
            res = requests.get(f"{self.api_url}/api/v1/blockchain/", timeout=5)
            if res.status_code == 200:
                return res.json()['blocks']
        except Exception as e:
            print(f"Get Chain Failed: {e}")
        return []

    def run(self):
        if not self.wait_for_api():
            return

        initial_chain = self.get_chain_stats()
        initial_height = len(initial_chain)
        print(f"Benchmark: Initial Block Height: {initial_height}")

        start_time = time.time()
        
        gen_thread = threading.Thread(target=self.load_generator)
        gen_thread.start()

        time.sleep(self.duration)
        
        self.stop_event.set()
        gen_thread.join()

        print("Benchmark: Load generation finished. Waiting for processing...")
        time.sleep(10) 

        end_time = time.time()
        final_chain = self.get_chain_stats()
        
        tx_count = 0
        for block in final_chain:
            if block['block_height'] >= initial_height:
                tx_count += max(0, len(block['transactions']) - 1)
                
        tps = tx_count / (end_time - start_time)
        
        print(f"--- Results ---")
        print(f"Total TX Confirmed: {tx_count}")
        print(f"Time Elapsed: {end_time - start_time:.2f}s")
        print(f"TPS: {tps:.2f}")
        
        data = {
            "mode": "AUTO_BENCHMARK",
            "tps": tps,
            "total_tx": tx_count
        }
        
        try:
            df = pd.DataFrame([data])
            df.to_csv(self.output_file, mode='a', header=False)
        except Exception as e:
            print(f"Failed to save results: {e}")

if __name__ == "__main__":
    bench = BenchmarkSuite()
    bench.run()