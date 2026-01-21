import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv('config/.env')

class DatabaseOperations:
    """Handle all database operations"""
    
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
    
    def get_connection(self):
        """Create and return database connection"""
        return psycopg2.connect(**self.connection_params)
    
    def get_city_id(self, city_name):
        """Get city_id from city name"""
        connection = self.get_connection()
        cursor = connection.cursor()
        
        cursor.execute(
            "SELECT city_id FROM cities WHERE city_name = %s",
            (city_name,)
        )
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        return result[0] if result else None
    
    def insert_air_quality_data(self, city_name, aqi, pm25, pm10, no2=None, so2=None, co=None, o3=None, source='manual'):
        """Insert air quality measurement"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            city_id = self.get_city_id(city_name)
            
            if not city_id:
                print(f"City {city_name} not found in database")
                return False
            
            insert_query = """
                INSERT INTO air_quality 
                (city_id, timestamp, aqi, pm25, pm10, no2, so2, co, o3, data_source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (city_id, timestamp) DO NOTHING;
            """
            
            cursor.execute(insert_query, (
                city_id,
                datetime.now(),
                aqi,
                pm25,
                pm10,
                no2,
                so2,
                co,
                o3,
                source
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            print(f"✓ Air quality data inserted for {city_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error inserting data: {e}")
            return False
    
    def insert_weather_data(self, city_name, temperature, humidity, wind_speed, pressure):
        """Insert weather data"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            city_id = self.get_city_id(city_name)
            
            insert_query = """
                INSERT INTO weather 
                (city_id, timestamp, temperature, humidity, wind_speed, pressure)
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            
            cursor.execute(insert_query, (
                city_id,
                datetime.now(),
                temperature,
                humidity,
                wind_speed,
                pressure
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            print(f"✓ Weather data inserted for {city_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error inserting weather data: {e}")
            return False
    
    def get_latest_aqi(self, city_name):
        """Get latest AQI for a city"""
        connection = self.get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        city_id = self.get_city_id(city_name)
        
        query = """
            SELECT * FROM air_quality
            WHERE city_id = %s
            ORDER BY timestamp DESC
            LIMIT 1;
        """
        
        cursor.execute(query, (city_id,))
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        return dict(result) if result else None
    
    def get_all_cities(self):
        """Get all cities from database"""
        connection = self.get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("SELECT * FROM cities ORDER BY city_name;")
        results = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return [dict(row) for row in results]