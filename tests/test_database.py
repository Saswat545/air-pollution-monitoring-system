import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.db_operations import DatabaseOperations

def test_database_operations():
    """Test all database operations"""
    
    print("=" * 50)
    print("Testing Database Operations")
    print("=" * 50)
    
    db = DatabaseOperations()
    
    # Test 1: Get all cities
    print("\n1. Testing: Get all cities")
    cities = db.get_all_cities()
    print(f"✓ Found {len(cities)} cities in database:")
    for city in cities:
        print(f"  - {city['city_name']}, {city['state']}")
    
    # Test 2: Get city ID
    print("\n2. Testing: Get city ID")
    city_id = db.get_city_id('Delhi')
    print(f"✓ Delhi city_id: {city_id}")
    
    # Test 3: Insert air quality data
    print("\n3. Testing: Insert air quality data")
    success = db.insert_air_quality_data(
        city_name='Delhi',
        aqi=287,
        pm25=145,
        pm10=198,
        no2=45,
        so2=12,
        co=1.2,
        o3=55,
        source='test'
    )
    
    if success:
        print("✓ Air quality data inserted successfully")
    
    # Test 4: Insert weather data
    print("\n4. Testing: Insert weather data")
    success = db.insert_weather_data(
        city_name='Delhi',
        temperature=28.5,
        humidity=45,
        wind_speed=12.3,
        pressure=1013.25
    )
    
    if success:
        print("✓ Weather data inserted successfully")
    
    # Test 5: Get latest AQI
    print("\n5. Testing: Get latest AQI")
    latest = db.get_latest_aqi('Delhi')
    if latest:
        print(f"✓ Latest AQI for Delhi: {latest['aqi']}")
        print(f"  PM2.5: {latest['pm25']}")
        print(f"  PM10: {latest['pm10']}")
        print(f"  Timestamp: {latest['timestamp']}")
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    test_database_operations()