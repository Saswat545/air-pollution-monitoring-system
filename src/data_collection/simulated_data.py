import random
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.database.db_operations import DatabaseOperations
import psycopg2

class SimulatedDataCollector:
    """Simulate air quality and weather data for testing"""
    
    def __init__(self):
        self.db = DatabaseOperations()
        self.cities = [
            'Delhi', 'Mumbai', 'Kolkata', 'Chennai',
            'Bangalore', 'Hyderabad', 'Pune', 'Ahmedabad'
        ]
    
    def generate_weather_data(self, city):
        """Generate realistic weather data"""
        base_temps = {
            'Delhi': 28, 'Mumbai': 32, 'Kolkata': 30,
            'Chennai': 34, 'Bangalore': 26, 'Hyderabad': 29,
            'Pune': 27, 'Ahmedabad': 31
        }
        
        return {
            'city': city,
            'temperature': base_temps[city] + random.uniform(-3, 3),
            'humidity': random.randint(40, 80),
            'wind_speed': random.uniform(5, 20),
            'pressure': random.uniform(1010, 1020)
        }
    
    def generate_aqi_data(self, city):
        """Generate realistic AQI data"""
        base_aqi = {
            'Delhi': 280, 'Mumbai': 155, 'Kolkata': 195,
            'Chennai': 130, 'Bangalore': 110, 'Hyderabad': 145,
            'Pune': 120, 'Ahmedabad': 175
        }
        
        aqi = base_aqi[city] + random.randint(-20, 20)
        pm25 = aqi * 0.5 + random.uniform(-10, 10)
        pm10 = aqi * 0.7 + random.uniform(-15, 15)
        
        return {
            'city': city,
            'aqi': aqi,
            'pm25': pm25,
            'pm10': pm10,
            'no2': random.uniform(30, 60),
            'so2': random.uniform(10, 25),
            'co': random.uniform(0.8, 2.5),
            'o3': random.uniform(40, 80)
        }
    
    def insert_data_with_matching_timestamp(self, city, timestamp):
        """Insert both weather and AQI data with the same timestamp"""
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            city_id = self.db.get_city_id(city)
            
            if not city_id:
                print(f"City {city} not found")
                return False
            
            # Generate data
            weather = self.generate_weather_data(city)
            aqi = self.generate_aqi_data(city)
            
            # Insert weather data
            weather_query = """
                INSERT INTO weather 
                (city_id, timestamp, temperature, humidity, wind_speed, pressure)
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            cursor.execute(weather_query, (
                city_id, timestamp, weather['temperature'], 
                weather['humidity'], weather['wind_speed'], weather['pressure']
            ))
            
            # Insert AQI data with same timestamp
            aqi_query = """
                INSERT INTO air_quality 
                (city_id, timestamp, aqi, pm25, pm10, no2, so2, co, o3, data_source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (city_id, timestamp) DO NOTHING;
            """
            cursor.execute(aqi_query, (
                city_id, timestamp, int(aqi['aqi']), aqi['pm25'], 
                aqi['pm10'], aqi['no2'], aqi['so2'], aqi['co'], 
                aqi['o3'], 'simulated'
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True
            
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def collect_all_data(self):
        """Collect simulated data for all cities"""
        timestamp = datetime.now()
        
        for city in self.cities:
            success = self.insert_data_with_matching_timestamp(city, timestamp)
            if not success:
                print(f"❌ Failed for {city}")

if __name__ == "__main__":
    collector = SimulatedDataCollector()
    
    print("=" * 60)
    print("🔄 Collecting data with matching timestamps")
    print("=" * 60)
    
    collector.collect_all_data()
    
    print("✅ Data collection complete!")