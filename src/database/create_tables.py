import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('config/.env')

def create_database_tables():
    """Create all necessary database tables"""
    
    try:
        # Connect to PostgreSQL
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        
        cursor = connection.cursor()
        
        print("Connected to database successfully!")
        print("Creating tables...")
        
        # Create Cities Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                city_id SERIAL PRIMARY KEY,
                city_name VARCHAR(100) UNIQUE NOT NULL,
                state VARCHAR(100),
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("✓ Cities table created")
        
        # Create Air Quality Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS air_quality (
                measurement_id SERIAL PRIMARY KEY,
                city_id INTEGER REFERENCES cities(city_id),
                timestamp TIMESTAMP NOT NULL,
                aqi INTEGER,
                pm25 DECIMAL(10, 2),
                pm10 DECIMAL(10, 2),
                no2 DECIMAL(10, 2),
                so2 DECIMAL(10, 2),
                co DECIMAL(10, 2),
                o3 DECIMAL(10, 2),
                data_source VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(city_id, timestamp)
            );
        """)
        print("✓ Air quality table created")
        
        # Create Weather Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather (
                weather_id SERIAL PRIMARY KEY,
                city_id INTEGER REFERENCES cities(city_id),
                timestamp TIMESTAMP NOT NULL,
                temperature DECIMAL(5, 2),
                humidity INTEGER,
                wind_speed DECIMAL(5, 2),
                wind_direction INTEGER,
                pressure DECIMAL(7, 2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("✓ Weather table created")
        
        # Create Predictions Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                prediction_id SERIAL PRIMARY KEY,
                city_id INTEGER REFERENCES cities(city_id),
                prediction_timestamp TIMESTAMP NOT NULL,
                predicted_aqi INTEGER,
                confidence_score DECIMAL(5, 4),
                model_version VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("✓ Predictions table created")
        
        # Create Alerts Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                alert_id SERIAL PRIMARY KEY,
                city_id INTEGER REFERENCES cities(city_id),
                alert_type VARCHAR(50),
                severity VARCHAR(20),
                aqi_value INTEGER,
                message TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                recipients_count INTEGER
            );
        """)
        print("✓ Alerts table created")
        
        # Insert initial cities data
        cities_data = [
            ('Delhi', 'Delhi', 28.6139, 77.2090),
            ('Mumbai', 'Maharashtra', 19.0760, 72.8777),
            ('Kolkata', 'West Bengal', 22.5726, 88.3639),
            ('Chennai', 'Tamil Nadu', 13.0827, 80.2707),
            ('Bangalore', 'Karnataka', 12.9716, 77.5946),
            ('Hyderabad', 'Telangana', 17.3850, 78.4867),
            ('Pune', 'Maharashtra', 18.5204, 73.8567),
            ('Ahmedabad', 'Gujarat', 23.0225, 72.5714)
        ]
        
        insert_query = """
            INSERT INTO cities (city_name, state, latitude, longitude)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (city_name) DO NOTHING;
        """
        
        cursor.executemany(insert_query, cities_data)
        print("✓ Initial cities data inserted")
        
        # Commit changes
        connection.commit()
        print("\n✅ All tables created successfully!")
        print(f"✅ {len(cities_data)} cities added to database")
        
        # Close connection
        cursor.close()
        connection.close()
        
    except Exception as error:
        print(f"❌ Error: {error}")

if __name__ == "__main__":
    create_database_tables()