import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.database.db_operations import DatabaseOperations
from src.models.aqi_predictor import AQIPredictor
from datetime import datetime
import psycopg2

class AlertSystem:
    """Generate and manage air quality alerts"""
    
    def __init__(self):
        self.db = DatabaseOperations()
        self.predictor = AQIPredictor()
        
        # Alert thresholds
        self.WARNING_THRESHOLD = 150  # Moderate
        self.DANGER_THRESHOLD = 200   # Poor
        self.SEVERE_THRESHOLD = 300   # Very Poor
    
    def get_aqi_category(self, aqi):
        """Get AQI category and severity"""
        if aqi <= 50:
            return "Good", "low"
        elif aqi <= 100:
            return "Satisfactory", "low"
        elif aqi <= 200:
            return "Moderate", "medium"
        elif aqi <= 300:
            return "Poor", "high"
        elif aqi <= 400:
            return "Very Poor", "severe"
        else:
            return "Severe", "severe"
    
    def get_health_message(self, aqi):
        """Get health advisory message"""
        if aqi <= 50:
            return "Air quality is good. Enjoy outdoor activities!"
        elif aqi <= 100:
            return "Air quality is acceptable. Sensitive individuals should limit prolonged outdoor activities."
        elif aqi <= 200:
            return "Sensitive groups should reduce prolonged outdoor exertion. General public should limit outdoor activities."
        elif aqi <= 300:
            return "⚠️ Everyone should avoid prolonged outdoor exertion. Wear N95 masks if going outside is necessary."
        elif aqi <= 400:
            return "🚨 Health alert! Avoid outdoor activities. Stay indoors with air purifiers. Use N95 masks outdoors."
        else:
            return "🆘 EMERGENCY! Avoid all outdoor activities. Stay indoors. Seal windows. Use air purifiers."
    
    def get_recommendations(self, aqi):
        """Get specific recommendations"""
        recommendations = []
        
        if aqi > 150:
            recommendations.append("• Keep windows and doors closed")
            recommendations.append("• Use air purifiers indoors")
        
        if aqi > 200:
            recommendations.append("• Avoid outdoor exercise")
            recommendations.append("• Wear N95 masks if going outside")
            recommendations.append("• Limit travel")
        
        if aqi > 300:
            recommendations.append("• Stay indoors as much as possible")
            recommendations.append("• Check on elderly and children")
            recommendations.append("• Keep emergency medications ready")
        
        return recommendations
    
    def save_alert_to_db(self, city_name, alert_type, severity, aqi_value, message):
        """Save alert to database"""
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            city_id = self.db.get_city_id(city_name)
            
            insert_query = """
                INSERT INTO alerts 
                (city_id, alert_type, severity, aqi_value, message, sent_at)
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            
            cursor.execute(insert_query, (
                city_id, alert_type, severity, aqi_value, message, datetime.now()
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True
        except Exception as e:
            print(f"Error saving alert: {e}")
            return False
    
    def check_city_alerts(self, city_name):
        """Check if alerts should be generated for a city"""
        latest = self.db.get_latest_aqi(city_name)
        
        if not latest:
            return None
        
        aqi = latest['aqi']
        category, severity = self.get_aqi_category(aqi)
        
        # Generate alert if AQI is above warning threshold
        if aqi >= self.WARNING_THRESHOLD:
            alert = {
                'city': city_name,
                'aqi': aqi,
                'category': category,
                'severity': severity,
                'pm25': latest['pm25'],
                'pm10': latest['pm10'],
                'health_message': self.get_health_message(aqi),
                'recommendations': self.get_recommendations(aqi),
                'timestamp': datetime.now()
            }
            
            # Determine alert type
            if aqi >= self.SEVERE_THRESHOLD:
                alert['alert_type'] = 'SEVERE ALERT'
            elif aqi >= self.DANGER_THRESHOLD:
                alert['alert_type'] = 'HIGH ALERT'
            else:
                alert['alert_type'] = 'WARNING'
            
            # Save to database
            self.save_alert_to_db(
                city_name, 
                alert['alert_type'], 
                severity, 
                aqi, 
                alert['health_message']
            )
            
            return alert
        
        return None
    
    def generate_all_alerts(self):
        """Generate alerts for all cities"""
        print("=" * 80)
        print("🚨 AIR QUALITY ALERT SYSTEM")
        print("=" * 80)
        print(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print()
        
        cities = self.db.get_all_cities()
        alerts = []
        
        for city in cities:
            alert = self.check_city_alerts(city['city_name'])
            if alert:
                alerts.append(alert)
        
        if not alerts:
            print("✅ NO ALERTS - All cities have acceptable air quality levels!")
            print("=" * 80)
            return []
        
        # Display alerts
        print(f"⚠️  {len(alerts)} ALERT(S) GENERATED")
        print("=" * 80)
        print()
        
        for i, alert in enumerate(alerts, 1):
            print(f"{'='*80}")
            print(f"ALERT #{i} - {alert['alert_type']}")
            print(f"{'='*80}")
            print(f"📍 Location: {alert['city']}")
            print(f"📊 Current AQI: {alert['aqi']} ({alert['category']})")
            print(f"⚠️  Severity: {alert['severity'].upper()}")
            print(f"🔬 PM2.5: {alert['pm25']:.1f} μg/m³ | PM10: {alert['pm10']:.1f} μg/m³")
            print()
            print(f"💬 Health Advisory:")
            print(f"   {alert['health_message']}")
            print()
            
            if alert['recommendations']:
                print(f"📋 Recommendations:")
                for rec in alert['recommendations']:
                    print(f"   {rec}")
            
            print(f"{'='*80}")
            print()
        
        return alerts
    
    def generate_daily_report(self):
        """Generate comprehensive daily report"""
        print("\n")
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 25 + "DAILY AIR QUALITY REPORT" + " " * 29 + "║")
        print("╚" + "═" * 78 + "╝")
        print(f"\n📅 Date: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
        print("\n" + "=" * 80)
        
        # Current status
        print("\n📊 CURRENT AQI STATUS - ALL CITIES")
        print("-" * 80)
        print(f"{'City':<15} {'AQI':<8} {'Category':<15} {'Status':<12} {'Alert Level'}")
        print("-" * 80)
        
        cities = self.db.get_all_cities()
        
        for city in cities:
            latest = self.db.get_latest_aqi(city['city_name'])
            if latest:
                aqi = latest['aqi']
                category, severity = self.get_aqi_category(aqi)
                
                if aqi < 150:
                    status = "✅ Safe"
                    alert_level = "None"
                elif aqi < 200:
                    status = "⚠️  Moderate"
                    alert_level = "Warning"
                elif aqi < 300:
                    status = "🔴 Poor"
                    alert_level = "High Alert"
                else:
                    status = "🆘 Severe"
                    alert_level = "Severe Alert"
                
                print(f"{city['city_name']:<15} {aqi:<8} {category:<15} {status:<12} {alert_level}")
        
        print("=" * 80)
        
        # Generate alerts
        print("\n🚨 ACTIVE ALERTS")
        print("=" * 80)
        alerts = self.generate_all_alerts()
        
        # Predictions
        print("\n🔮 AQI PREDICTIONS (Next Period)")
        print("=" * 80)
        print(f"{'City':<15} {'Current':<10} {'Predicted':<12} {'Change':<10} {'Trend'}")
        print("-" * 80)
        
        for city in cities:
            try:
                self.predictor.load_model(city['city_name'])
                prediction = self.predictor.predict_next_aqi(city['city_name'])
                
                if prediction:
                    trend = "↑ Worsening" if prediction['change'] > 5 else "↓ Improving" if prediction['change'] < -5 else "→ Stable"
                    change_str = f"{prediction['change']:+d}"
                    print(f"{city['city_name']:<15} {prediction['current_aqi']:<10} {prediction['predicted_aqi']:<12} {change_str:<10} {trend}")
            except:
                print(f"{city['city_name']:<15} {'N/A':<10} {'N/A':<12} {'N/A':<10} N/A")
        
        print("=" * 80)
        print("\n✅ REPORT GENERATED SUCCESSFULLY")
        print("=" * 80)
        print()

if __name__ == "__main__":
    alert_system = AlertSystem()
    alert_system.generate_daily_report()