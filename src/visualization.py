import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.db_operations import DatabaseOperations
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pandas as pd

class DataVisualizer:
    """Create visualizations for air quality data"""
    
    def __init__(self):
        self.db = DatabaseOperations()
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
    
    def get_aqi_trends(self, city_name, limit=50):
        """Get AQI trends for a city"""
        connection = self.db.get_connection()
        
        query = """
            SELECT timestamp, aqi, pm25, pm10
            FROM air_quality
            WHERE city_id = (SELECT city_id FROM cities WHERE city_name = %s)
            ORDER BY timestamp DESC
            LIMIT %s;
        """
        
        df = pd.read_sql(query, connection, params=(city_name, limit))
        connection.close()
        
        # Reverse to show oldest to newest
        df = df.iloc[::-1].reset_index(drop=True)
        return df
    
    def plot_aqi_trend(self, city_name='Delhi'):
        """Plot AQI trend for a city"""
        df = self.get_aqi_trends(city_name, limit=50)
        
        if df.empty:
            print(f"No data found for {city_name}")
            return
        
        plt.figure(figsize=(14, 6))
        
        plt.plot(df.index, df['aqi'], marker='o', linewidth=2, markersize=6, color='#e74c3c', label='AQI')
        
        # Add AQI category zones
        plt.axhspan(0, 50, alpha=0.1, color='green', label='Good')
        plt.axhspan(50, 100, alpha=0.1, color='yellow', label='Satisfactory')
        plt.axhspan(100, 200, alpha=0.1, color='orange', label='Moderate')
        plt.axhspan(200, 300, alpha=0.1, color='red', label='Poor')
        plt.axhspan(300, 500, alpha=0.1, color='purple', label='Very Poor')
        
        plt.title(f'Air Quality Index Trend - {city_name}', fontsize=16, fontweight='bold')
        plt.xlabel('Sample Number', fontsize=12)
        plt.ylabel('AQI Value', fontsize=12)
        plt.legend(loc='upper right')
        plt.grid(True, alpha=0.3)
        
        # Save figure
        os.makedirs('data/visualizations', exist_ok=True)
        plt.savefig(f'data/visualizations/aqi_trend_{city_name.lower()}.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: data/visualizations/aqi_trend_{city_name.lower()}.png")
        
        plt.show()
    
    def plot_all_cities_comparison(self):
        """Compare current AQI across all cities"""
        cities = self.db.get_all_cities()
        
        city_names = []
        aqi_values = []
        colors = []
        
        for city in cities:
            latest = self.db.get_latest_aqi(city['city_name'])
            if latest:
                city_names.append(city['city_name'])
                aqi_values.append(latest['aqi'])
                
                # Color code by category
                if latest['aqi'] <= 100:
                    colors.append('#27ae60')  # Green
                elif latest['aqi'] <= 200:
                    colors.append('#f39c12')  # Orange
                elif latest['aqi'] <= 300:
                    colors.append('#e74c3c')  # Red
                else:
                    colors.append('#8e44ad')  # Purple
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(city_names, aqi_values, color=colors, edgecolor='black', linewidth=1.2)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Add reference lines
        plt.axhline(y=100, color='yellow', linestyle='--', linewidth=1, alpha=0.7, label='Satisfactory (100)')
        plt.axhline(y=200, color='orange', linestyle='--', linewidth=1, alpha=0.7, label='Moderate (200)')
        plt.axhline(y=300, color='red', linestyle='--', linewidth=1, alpha=0.7, label='Poor (300)')
        
        plt.title('Current Air Quality Index - All Cities', fontsize=16, fontweight='bold')
        plt.xlabel('City', fontsize=12)
        plt.ylabel('AQI Value', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.grid(True, axis='y', alpha=0.3)
        
        os.makedirs('data/visualizations', exist_ok=True)
        plt.savefig('data/visualizations/cities_comparison.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: data/visualizations/cities_comparison.png")
        
        plt.show()
    
    def plot_pm_comparison(self, city_name='Delhi'):
        """Compare PM2.5 and PM10 levels"""
        df = self.get_aqi_trends(city_name, limit=30)
        
        if df.empty:
            print(f"No data found for {city_name}")
            return
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # PM2.5
        ax1.plot(df.index, df['pm25'], marker='o', color='#e74c3c', linewidth=2, markersize=6)
        ax1.axhline(y=60, color='orange', linestyle='--', linewidth=1.5, label='Safe Limit (60 μg/m³)')
        ax1.fill_between(df.index, df['pm25'], alpha=0.3, color='#e74c3c')
        ax1.set_title(f'PM2.5 Levels - {city_name}', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Sample Number', fontsize=11)
        ax1.set_ylabel('PM2.5 (μg/m³)', fontsize=11)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # PM10
        ax2.plot(df.index, df['pm10'], marker='s', color='#3498db', linewidth=2, markersize=6)
        ax2.axhline(y=100, color='orange', linestyle='--', linewidth=1.5, label='Safe Limit (100 μg/m³)')
        ax2.fill_between(df.index, df['pm10'], alpha=0.3, color='#3498db')
        ax2.set_title(f'PM10 Levels - {city_name}', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Sample Number', fontsize=11)
        ax2.set_ylabel('PM10 (μg/m³)', fontsize=11)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        os.makedirs('data/visualizations', exist_ok=True)
        plt.savefig(f'data/visualizations/pm_comparison_{city_name.lower()}.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: data/visualizations/pm_comparison_{city_name.lower()}.png")
        
        plt.show()
    
    def plot_correlation_heatmap(self):
        """Plot correlation between pollutants and weather"""
        connection = self.db.get_connection()
        
        query = """
            SELECT 
                aq.aqi, aq.pm25, aq.pm10, aq.no2, aq.so2, aq.co, aq.o3,
                w.temperature, w.humidity, w.wind_speed, w.pressure
            FROM air_quality aq
            JOIN weather w ON aq.city_id = w.city_id 
                AND DATE_TRUNC('minute', aq.timestamp) = DATE_TRUNC('minute', w.timestamp)
            LIMIT 100;
        """
        
        df = pd.read_sql(query, connection)
        connection.close()
        
        if df.empty:
            print("No data found for correlation analysis")
            return
        
        # Calculate correlation
        correlation = df.corr()
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, linewidths=1, linecolor='white',
                   cbar_kws={'label': 'Correlation Coefficient'})
        
        plt.title('Correlation Between Pollutants and Weather Factors', 
                 fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        
        os.makedirs('data/visualizations', exist_ok=True)
        plt.savefig('data/visualizations/correlation_heatmap.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: data/visualizations/correlation_heatmap.png")
        
        plt.show()
    
    def generate_all_visualizations(self):
        """Generate all visualizations"""
        print("=" * 70)
        print("📊 GENERATING DATA VISUALIZATIONS")
        print("=" * 70)
        print()
        
        print("1. Creating city comparison chart...")
        self.plot_all_cities_comparison()
        print()
        
        print("2. Creating AQI trend for Delhi...")
        self.plot_aqi_trend('Delhi')
        print()
        
        print("3. Creating AQI trend for Mumbai...")
        self.plot_aqi_trend('Mumbai')
        print()
        
        print("4. Creating PM comparison for Delhi...")
        self.plot_pm_comparison('Delhi')
        print()
        
        print("5. Creating correlation heatmap...")
        self.plot_correlation_heatmap()
        print()
        
        print("=" * 70)
        print("✅ ALL VISUALIZATIONS GENERATED!")
        print("📁 Location: data/visualizations/")
        print("=" * 70)

if __name__ == "__main__":
    visualizer = DataVisualizer()
    visualizer.generate_all_visualizations()