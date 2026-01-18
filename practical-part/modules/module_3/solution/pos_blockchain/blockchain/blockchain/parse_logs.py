import re
import pandas as pd
import matplotlib.pyplot as plt

LOG_FILE = "pos_logs.txt" # You save docker logs here: docker-compose logs > node_logs.txt

def parse_metrics():
    resources = []
    propagation = []
    
    with open(LOG_FILE, 'r') as f:
        for line in f:
            # Regex for Resource
            # Log format: BENCHMARK_RESOURCES: CPU: 12.5% | RAM: 45.20MB
            res_match = re.search(r"BENCHMARK_RESOURCES: CPU: ([\d.]+)% \| RAM: ([\d.]+)MB", line)
            if res_match:
                resources.append({
                    "cpu": float(res_match.group(1)),
                    "ram": float(res_match.group(2))
                })

            # Regex for Propagation
            # Log format: BENCHMARK_PROPAGATION: Block 5 Delay: 0.2341s
            prop_match = re.search(r"BENCHMARK_PROPAGATION: Block (\d+) Delay: ([\d.]+)s", line)
            if prop_match:
                propagation.append({
                    "block": int(prop_match.group(1)),
                    "delay": float(prop_match.group(2))
                })

    return pd.DataFrame(resources), pd.DataFrame(propagation)

def plot_data(res_df, prop_df, title="Proof of Stake"):
    # 1. CPU Usage
    plt.figure(figsize=(10, 5))
    plt.plot(res_df['cpu'], label='CPU %', color='orange')
    plt.title(f"{title} - CPU Utilization")
    plt.ylabel("Percentage")
    plt.tight_layout()
    plt.savefig(f"{title}_cpu_metrics.png")
    plt.close()
    
    # 2. RAM Usage
    plt.figure(figsize=(10, 5))
    plt.plot(res_df['ram'], label='RAM (MB)', color='blue')
    plt.title(f"{title} - Memory Usage")
    plt.ylabel("MB")
    plt.tight_layout()
    plt.savefig(f"{title}_ram_metrics.png")
    plt.close()
    
    # 3. Latency
    if not prop_df.empty:
        plt.figure(figsize=(10, 5))
        plt.bar(prop_df['block'], prop_df['delay'], color='green')
        plt.title(f"{title} - Block Propagation Latency")
        plt.xlabel("Block Height")
        plt.ylabel("Seconds")
        plt.tight_layout()
        plt.savefig(f"{title}_latency_metrics.png")
        plt.close()

if __name__ == "__main__":
    res_df, prop_df = parse_metrics()
    print(f"Avg CPU: {res_df['cpu'].mean():.2f}%")
    print(f"Avg RAM: {res_df['ram'].mean():.2f} MB")
    if not prop_df.empty:
        print(f"Avg Latency: {prop_df['delay'].mean():.4f}s")
    
    plot_data(res_df, prop_df, "PoS_Benchmark")
