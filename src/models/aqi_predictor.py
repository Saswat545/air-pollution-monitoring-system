import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.database.db_operations import DatabaseOperations
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
from datetime import datetime, timedelta

class AQIPredictor:
    """Machine Learning model to predict AQI"""
    
    def __init__(self):
        self.db = DatabaseOperations()
        self.model = None
        self.feature_columns = None
    
    def prepare_data(self, city_name, limit=100):
        """Prepare data for training"""
        connection = self.db.get_connection()
        
        query = """
            SELECT 
                aq.timestamp,
                aq.aqi,
                aq.pm25,
                aq.pm10,
                aq.no2,
                aq.so2,
                aq.co,
                aq.o3,
                w.temperature,
                w.humidity,
                w.wind_speed,
                w.pressure
            FROM air_quality aq
            JOIN weather w ON aq.city_id = w.city_id 
                AND DATE_TRUNC('second', aq.timestamp) = DATE_TRUNC('second', w.timestamp)
            WHERE aq.city_id = (SELECT city_id FROM cities WHERE city_name = %s)
            ORDER BY aq.timestamp ASC
            LIMIT %s;
        """
        
        df = pd.read_sql(query, connection, params=(city_name, limit))
        connection.close()
        
        if df.empty:
            print(f"No data found for {city_name}")
            return None
        
        # Create time-based features
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
        
        # Create lag features (previous values)
        df['aqi_lag_1'] = df['aqi'].shift(1)
        df['pm25_lag_1'] = df['pm25'].shift(1)
        df['pm10_lag_1'] = df['pm10'].shift(1)
        
        # Create rolling averages
        df['aqi_rolling_3'] = df['aqi'].rolling(window=3).mean()
        df['pm25_rolling_3'] = df['pm25'].rolling(window=3).mean()
        
        # Drop rows with NaN (from lag features)
        df = df.dropna()
        
        return df
    
    def train_model(self, city_name='Delhi'):
        """Train the prediction model"""
        print("=" * 70)
        print(f"🤖 TRAINING AQI PREDICTION MODEL FOR {city_name.upper()}")
        print("=" * 70)
        print()
        
        # Prepare data
        print("📊 Preparing data...")
        df = self.prepare_data(city_name, limit=200)
        
        if df is None or len(df) < 10:
            print("❌ Not enough data to train model!")
            return False
        
        print(f"✓ Loaded {len(df)} samples")
        print()
        
        # Define features and target
        self.feature_columns = [
            'pm25', 'pm10', 'no2', 'so2', 'co', 'o3',
            'temperature', 'humidity', 'wind_speed', 'pressure',
            'hour', 'day_of_week',
            'aqi_lag_1', 'pm25_lag_1', 'pm10_lag_1',
            'aqi_rolling_3', 'pm25_rolling_3'
        ]
        
        X = df[self.feature_columns]
        y = df['aqi']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"📈 Training set: {len(X_train)} samples")
        print(f"📉 Test set: {len(X_test)} samples")
        print()
        
        # Train model
        print("🔄 Training Random Forest model...")
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        print("✓ Model trained successfully!")
        print()
        
        # Evaluate model
        print("📊 Model Performance:")
        print("-" * 70)
        
        # Training set performance
        train_pred = self.model.predict(X_train)
        train_mae = mean_absolute_error(y_train, train_pred)
        train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
        train_r2 = r2_score(y_train, train_pred)
        
        print(f"Training Set:")
        print(f"  MAE (Mean Absolute Error): {train_mae:.2f}")
        print(f"  RMSE (Root Mean Squared Error): {train_rmse:.2f}")
        print(f"  R² Score: {train_r2:.4f}")
        print()
        
        # Test set performance
        test_pred = self.model.predict(X_test)
        test_mae = mean_absolute_error(y_test, test_pred)
        test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
        test_r2 = r2_score(y_test, test_pred)
        
        print(f"Test Set:")
        print(f"  MAE (Mean Absolute Error): {test_mae:.2f}")
        print(f"  RMSE (Root Mean Squared Error): {test_rmse:.2f}")
        print(f"  R² Score: {test_r2:.4f}")
        print()
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("🎯 Top 5 Most Important Features:")
        print("-" * 70)
        for idx, row in feature_importance.head(5).iterrows():
            print(f"  {row['feature']:<20} {row['importance']:.4f}")
        print()
        
        # Save model
        os.makedirs('data/models', exist_ok=True)
        model_path = f'data/models/aqi_model_{city_name.lower()}.pkl'
        
        with open(model_path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'feature_columns': self.feature_columns,
                'city': city_name,
                'trained_date': datetime.now(),
                'performance': {
                    'test_mae': test_mae,
                    'test_rmse': test_rmse,
                    'test_r2': test_r2
                }
            }, f)
        
        print(f"💾 Model saved: {model_path}")
        print()
        print("=" * 70)
        print("✅ MODEL TRAINING COMPLETE!")
        print("=" * 70)
        
        return True
    
    def load_model(self, city_name='Delhi'):
        """Load a saved model"""
        model_path = f'data/models/aqi_model_{city_name.lower()}.pkl'
        
        if not os.path.exists(model_path):
            print(f"❌ No saved model found for {city_name}")
            return False
        
        with open(model_path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.feature_columns = data['feature_columns']
        
        print(f"✓ Model loaded for {city_name}")
        return True
    
    def predict_next_aqi(self, city_name='Delhi'):
        """Predict next AQI value"""
        if self.model is None:
            if not self.load_model(city_name):
                print("Training new model...")
                self.train_model(city_name)
        
        # Get latest data
        df = self.prepare_data(city_name, limit=10)
        
        if df is None or len(df) == 0:
            print("❌ No data available for prediction")
            return None
        
        # Get the latest row
        latest = df.iloc[-1]
        
        # Prepare features
        features = latest[self.feature_columns].values.reshape(1, -1)
        
        # Make prediction
        predicted_aqi = self.model.predict(features)[0]
        
        return {
            'city': city_name,
            'current_aqi': int(latest['aqi']),
            'predicted_aqi': int(predicted_aqi),
            'change': int(predicted_aqi - latest['aqi']),
            'timestamp': datetime.now()
        }
    
    def predict_all_cities(self):
        """Predict AQI for all cities"""
        print("=" * 70)
        print("🔮 AQI PREDICTIONS FOR ALL CITIES")
        print("=" * 70)
        print()
        
        cities = ['Delhi', 'Mumbai', 'Kolkata', 'Chennai', 
                 'Bangalore', 'Hyderabad', 'Pune', 'Ahmedabad']
        
        predictions = []
        
        for city in cities:
            print(f"Predicting for {city}...", end=" ")
            
            try:
                # Train model if not exists
                model_path = f'data/models/aqi_model_{city.lower()}.pkl'
                if not os.path.exists(model_path):
                    self.train_model(city)
                else:
                    self.load_model(city)
                
                prediction = self.predict_next_aqi(city)
                
                if prediction:
                    predictions.append(prediction)
                    trend = "↑" if prediction['change'] > 0 else "↓" if prediction['change'] < 0 else "→"
                    print(f"Current: {prediction['current_aqi']} → Predicted: {prediction['predicted_aqi']} {trend}")
                else:
                    print("❌ Failed")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        print()
        print("=" * 70)
        print("📊 PREDICTION SUMMARY")
        print("=" * 70)
        print(f"{'City':<15} {'Current AQI':<15} {'Predicted AQI':<15} {'Change':<10} {'Trend'}")
        print("-" * 70)
        
        for pred in predictions:
            trend = "Increasing ↑" if pred['change'] > 5 else "Decreasing ↓" if pred['change'] < -5 else "Stable →"
            change_str = f"{pred['change']:+d}"
            print(f"{pred['city']:<15} {pred['current_aqi']:<15} {pred['predicted_aqi']:<15} {change_str:<10} {trend}")
        
        print("=" * 70)
        print("✅ PREDICTIONS COMPLETE!")
        print("=" * 70)
        
        return predictions

if __name__ == "__main__":
    predictor = AQIPredictor()
    
    # Train model for Delhi
    print("\n🎯 Step 1: Training model for Delhi\n")
    predictor.train_model('Delhi')
    
    print("\n" + "="*70 + "\n")
    
    # Make predictions for all cities
    print("🎯 Step 2: Making predictions for all cities\n")
    predictor.predict_all_cities()