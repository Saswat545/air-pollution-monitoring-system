import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.data_collection.simulated_data import SimulatedDataCollector
import time
from datetime import datetime

def collect_multiple_samples(num_samples=10, delay_seconds=2):
    """Collect multiple samples to simulate historical data"""
    
    print("=" * 70)
    print("🔄 COLLECTING HISTORICAL DATA SAMPLES")
    print("=" * 70)
    print(f"Samples to collect: {num_samples}")
    print(f"Delay between samples: {delay_seconds} seconds")
    print("=" * 70)
    print()
    
    collector = SimulatedDataCollector()
    
    for i in range(1, num_samples + 1):
        print(f"\n📊 Collecting Sample {i}/{num_samples}")
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        print("-" * 70)
        
        collector.collect_all_data()
        
        if i < num_samples:
            print(f"\n⏳ Waiting {delay_seconds} seconds before next collection...")
            time.sleep(delay_seconds)
    
    print("\n" + "=" * 70)
    print(f"✅ COMPLETED! Collected {num_samples} samples for all cities")
    print("=" * 70)

if __name__ == "__main__":
    # Collect 10 samples with 2 seconds between each
    collect_multiple_samples(num_samples=10, delay_seconds=2)