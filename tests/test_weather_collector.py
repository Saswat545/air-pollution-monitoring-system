import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_collection.weather_collector import WeatherCollector

def test_weather_collector():
    """Test weather data collection"""
    
    print("\n🧪 Testing Weather Collector\n")
    
    collector = WeatherCollector()
    
    # Test single city
    print("Testing single city fetch (Delhi):")
    weather = collector.fetch_weather('Delhi')
    
    if weather:
        print("✅ Weather fetch successful!")
        print(f"   Temperature: {weather['temperature']}°C")
        print(f"   Humidity: {weather['humidity']}%")
        print(f"   Wind Speed: {weather['wind_speed']} m/s")
        print(f"   Pressure: {weather['pressure']} hPa")
        print(f"   Description: {weather['description']}")
    else:
        print("❌ Weather fetch failed!")
        print("Make sure you added your API key to config/.env")
    
    print("\n" + "="*50)
    input("\nPress Enter to collect data for all cities...")
    
    # Test all cities
    collector.collect_all_cities()

if __name__ == "__main__":
    test_weather_collector()