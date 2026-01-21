import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.data_collection.simulated_data import SimulatedDataCollector
import time
from datetime import datetime

def collect_training_data(num_samples=50):
    """Collect data for training ML model"""
    
    print("=" * 70)
    print("🎯 COLLECTING TRAINING DATA FOR ML MODEL")
    print("=" * 70)
    print(f"Samples to collect: {num_samples}")
    print("This will take about {:.0f} seconds".format(num_samples * 1))
    print("=" * 70)
    print()
    
    collector = SimulatedDataCollector()
    
    for i in range(1, num_samples + 1):
        print(f"Collecting sample {i}/{num_samples}... ", end="", flush=True)
        
        collector.collect_all_data()
        
        print("✓")
        
        if i < num_samples:
            time.sleep(1)  # Wait 1 second between samples
    
    print()
    print("=" * 70)
    print(f"✅ COMPLETE! Collected {num_samples} samples for 8 cities")
    print(f"📊 Total data points: {num_samples * 8 * 2} (weather + AQI)")
    print("=" * 70)

if __name__ == "__main__":
    collect_training_data(num_samples=50)