import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.database.db_operations import DatabaseOperations

load_dotenv('config/.env')

class WeatherCollector:
    """Collect weather data from OpenWeatherMap API"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.db = DatabaseOperations()
        
        self.cities = [
            'Delhi', 'Mumbai', 'Kolkata', 'Chennai',
            'Bangalore', 'Hyderabad', 'Pune', 'Ahmedabad'
        ]
    
    def fetch_weather(self, city):
        """Fetch weather data for a specific city"""
        try:
            params = {
                'q': f'{city},IN',
                'appid': self.api_key,
                'units': 'metric'  # For Celsius
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            weather_info = {
                'city': city,
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'description': data['weather'][0]['description'],
                'timestamp': datetime.now()
            }
            
            return weather_info
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching weather for {city}: {e}")
            return None
        except KeyError as e:
            print(f"❌ Error parsing weather data for {city}: {e}")
            return None
    
    def collect_all_cities(self):
        """Collect weather data for all cities"""
        print("=" * 60)
        print("🌤️  Starting Weather Data Collection")
        print("=" * 60)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        collected = 0
        failed = 0
        
        for city in self.cities:
            print(f"Fetching weather for {city}...", end=" ")
            
            weather = self.fetch_weather(city)
            
            if weather:
                # Store in database
                success = self.db.insert_weather_data(
                    city_name=city,
                    temperature=weather['temperature'],
                    humidity=weather['humidity'],
                    wind_speed=weather['wind_speed'],
                    pressure=weather['pressure']
                )
                
                if success:
                    print(f"✓ {weather['temperature']}°C, {weather['humidity']}% humidity")
                    collected += 1
                else:
                    print("❌ Failed to store in database")
                    failed += 1
            else:
                print("❌ Failed to fetch")
                failed += 1
        
        print()
        print("=" * 60)
        print(f"✅ Collection Complete!")
        print(f"   Collected: {collected}/{len(self.cities)}")
        print(f"   Failed: {failed}/{len(self.cities)}")
        print("=" * 60)
        
        return collected, failed

if __name__ == "__main__":
    collector = WeatherCollector()
    collector.collect_all_cities()