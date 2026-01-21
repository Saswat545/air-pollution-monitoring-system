import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.db_operations import DatabaseOperations
import pandas as pd
from datetime import datetime, timedelta

class DataAnalyzer:
    """Analyze air quality and weather data"""
    
    def __init__(self):
        self.db = DatabaseOperations()
    
    def get_current_aqi_all_cities(self):
        """Get current AQI for all cities"""
        print("=" * 70)
        print("📊 CURRENT AIR QUALITY INDEX - ALL CITIES")
        print("=" * 70)
        print(f"{'City':<15} {'AQI':<8} {'Category':<15} {'PM2.5':<10} {'PM10':<10}")
        print("-" * 70)
        
        cities = self.db.get_all_cities()
        
        for city in cities:
            latest = self.db.get_latest_aqi(city['city_name'])
            if latest:
                aqi = latest['aqi']
                category = self.get_aqi_category(aqi)
                print(f"{city['city_name']:<15} {aqi:<8} {category:<15} {latest['pm25']:<10.1f} {latest['pm10']:<10.1f}")
        
        print("=" * 70)
    
    def get_aqi_category(self, aqi):
        """Get AQI category"""
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Satisfactory"
        elif aqi <= 200:
            return "Moderate"
        elif aqi <= 300:
            return "Poor"
        elif aqi <= 400:
            return "Very Poor"
        else:
            return "Severe"
    
    def get_weather_all_cities(self):
        """Get current weather for all cities"""
        print("\n" + "=" * 70)
        print("🌤️  CURRENT WEATHER - ALL CITIES")
        print("=" * 70)
        print(f"{'City':<15} {'Temp(°C)':<12} {'Humidity(%)':<15} {'Wind(m/s)':<12}")
        print("-" * 70)
        
        connection = self.db.get_connection()
        cursor = connection.cursor()
        
        query = """
            SELECT c.city_name, w.temperature, w.humidity, w.wind_speed
            FROM weather w
            JOIN cities c ON w.city_id = c.city_id
            WHERE w.timestamp = (
                SELECT MAX(timestamp) 
                FROM weather w2 
                WHERE w2.city_id = w.city_id
            )
            ORDER BY c.city_name;
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        for row in results:
            city, temp, humidity, wind = row
            print(f"{city:<15} {temp:<12.1f} {humidity:<15} {wind:<12.1f}")
        
        cursor.close()
        connection.close()
        
        print("=" * 70)
    
    def get_pollution_statistics(self):
        """Get pollution statistics"""
        print("\n" + "=" * 70)
        print("📈 POLLUTION STATISTICS")
        print("=" * 70)
        
        connection = self.db.get_connection()
        cursor = connection.cursor()
        
        # Most polluted city
        query = """
            SELECT c.city_name, aq.aqi
            FROM air_quality aq
            JOIN cities c ON aq.city_id = c.city_id
            WHERE aq.timestamp = (
                SELECT MAX(timestamp) 
                FROM air_quality aq2 
                WHERE aq2.city_id = aq.city_id
            )
            ORDER BY aq.aqi DESC
            LIMIT 1;
        """
        cursor.execute(query)
        most_polluted = cursor.fetchone()
        
        # Least polluted city
        query = """
            SELECT c.city_name, aq.aqi
            FROM air_quality aq
            JOIN cities c ON aq.city_id = c.city_id
            WHERE aq.timestamp = (
                SELECT MAX(timestamp) 
                FROM air_quality aq2 
                WHERE aq2.city_id = aq.city_id
            )
            ORDER BY aq.aqi ASC
            LIMIT 1;
        """
        cursor.execute(query)
        least_polluted = cursor.fetchone()
        
        # Average AQI
        query = """
            SELECT AVG(aq.aqi)
            FROM air_quality aq
            WHERE aq.timestamp = (
                SELECT MAX(timestamp) 
                FROM air_quality aq2 
                WHERE aq2.city_id = aq.city_id
            );
        """
        cursor.execute(query)
        avg_aqi = cursor.fetchone()[0]
        
        # Cities with dangerous AQI (>200)
        query = """
            SELECT COUNT(DISTINCT c.city_name)
            FROM air_quality aq
            JOIN cities c ON aq.city_id = c.city_id
            WHERE aq.aqi > 200
            AND aq.timestamp = (
                SELECT MAX(timestamp) 
                FROM air_quality aq2 
                WHERE aq2.city_id = aq.city_id
            );
        """
        cursor.execute(query)
        dangerous_count = cursor.fetchone()[0]
        
        cursor.close()
        connection.close()
        
        print(f"🔴 Most Polluted: {most_polluted[0]} (AQI: {most_polluted[1]})")
        print(f"🟢 Least Polluted: {least_polluted[0]} (AQI: {least_polluted[1]})")
        print(f"📊 Average AQI: {avg_aqi:.1f}")
        print(f"⚠️  Cities with Dangerous AQI (>200): {dangerous_count}")
        print("=" * 70)
    
    def show_health_alerts(self):
        """Show health alerts for high pollution cities"""
        print("\n" + "=" * 70)
        print("🚨 HEALTH ALERTS")
        print("=" * 70)
        
        cities = self.db.get_all_cities()
        alerts_found = False
        
        for city in cities:
            latest = self.db.get_latest_aqi(city['city_name'])
            if latest and latest['aqi'] > 200:
                alerts_found = True
                category = self.get_aqi_category(latest['aqi'])
                advice = self.get_health_advice(latest['aqi'])
                
                print(f"\n⚠️  ALERT: {city['city_name']}")
                print(f"   AQI: {latest['aqi']} ({category})")
                print(f"   {advice}")
        
        if not alerts_found:
            print("✅ No health alerts at this time. Air quality is acceptable in all cities.")
        
        print("=" * 70)
    
    def get_health_advice(self, aqi):
        """Get health advice based on AQI"""
        if aqi <= 50:
            return "Air quality is good. Ideal for outdoor activities."
        elif aqi <= 100:
            return "Air quality is acceptable. Sensitive individuals should limit prolonged outdoor exertion."
        elif aqi <= 200:
            return "Sensitive groups should reduce prolonged outdoor exertion."
        elif aqi <= 300:
            return "Everyone should avoid prolonged outdoor exertion. Use N95 masks if going outside."
        elif aqi <= 400:
            return "Health alert! Avoid outdoor activities. Use air purifiers indoors."
        else:
            return "Emergency! Stay indoors. Avoid all outdoor activities."
    
    def run_full_analysis(self):
        """Run complete analysis"""
        print("\n")
        print("╔" + "═" * 68 + "╗")
        print("║" + " " * 15 + "AIR POLLUTION MONITORING SYSTEM" + " " * 22 + "║")
        print("║" + " " * 20 + "Data Analysis Report" + " " * 28 + "║")
        print("╚" + "═" * 68 + "╝")
        print(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        self.get_current_aqi_all_cities()
        self.get_weather_all_cities()
        self.get_pollution_statistics()
        self.show_health_alerts()
        
        print("\n" + "=" * 70)
        print("✅ Analysis Complete!")
        print("=" * 70 + "\n")

if __name__ == "__main__":
    analyzer = DataAnalyzer()
    analyzer.run_full_analysis()