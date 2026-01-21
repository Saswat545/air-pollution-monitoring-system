import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_collection.weather_collector import WeatherCollector
from src.data_collection.simulated_data import SimulatedDataCollector
from src.data_analysis import DataAnalyzer
from src.models.aqi_predictor import AQIPredictor
from src.alerts.alert_system import AlertSystem
from src.alerts.email_alerts import EmailAlerts
from datetime import datetime
import time
import schedule

class AirPollutionSystem:
    """Main system controller"""
    
    def __init__(self, use_real_api=False):
        self.use_real_api = use_real_api
        self.weather_collector = WeatherCollector()
        self.simulated_collector = SimulatedDataCollector()
        self.analyzer = DataAnalyzer()
        self.predictor = AQIPredictor()
        self.alert_system = AlertSystem()
        self.email_alerts = EmailAlerts()
        
        print("=" * 70)
        print("🌍 AIR POLLUTION MONITORING SYSTEM - INITIALIZED")
        print("=" * 70)
        print(f"Mode: {'REAL API' if use_real_api else 'SIMULATED DATA'}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        print()
    
    def collect_data(self):
        """Collect data from API or simulate"""
        print(f"\n⏰ [{datetime.now().strftime('%H:%M:%S')}] Collecting data...")
        
        if self.use_real_api:
            # Try real API
            try:
                collected, failed = self.weather_collector.collect_all_cities()
                if collected > 0:
                    print(f"✅ Collected real data for {collected} cities")
                    return True
                else:
                    print("⚠️ Real API failed, using simulated data")
                    self.simulated_collector.collect_all_data()
                    return True
            except Exception as e:
                print(f"❌ API Error: {e}")
                print("⚠️ Falling back to simulated data")
                self.simulated_collector.collect_all_data()
                return True
        else:
            # Use simulated data
            self.simulated_collector.collect_all_data()
            print("✅ Simulated data collected")
            return True
    
    def analyze_and_alert(self):
        """Analyze data and send alerts if needed"""
        print(f"\n📊 [{datetime.now().strftime('%H:%M:%S')}] Analyzing data...")
        
        # Check for alerts
        alerts = []
        cities = self.analyzer.db.get_all_cities()
        
        for city in cities:
            alert = self.alert_system.check_city_alerts(city['city_name'])
            if alert:
                alerts.append(alert)
        
        if alerts:
            print(f"🚨 {len(alerts)} alert(s) detected!")
            
            # Send email for each high/severe alert
            for alert in alerts:
                if alert['severity'] in ['high', 'severe']:
                    print(f"📧 Sending email alert for {alert['city']}...")
                    self.email_alerts.send_alert(
                        city=alert['city'],
                        aqi=alert['aqi'],
                        category=alert['category'],
                        health_message=alert['health_message']
                    )
        else:
            print("✅ No alerts - Air quality acceptable")
    
    def generate_predictions(self):
        """Generate ML predictions"""
        print(f"\n🔮 [{datetime.now().strftime('%H:%M:%S')}] Generating predictions...")
        
        cities = ['Delhi', 'Mumbai', 'Kolkata']  # Predict for major cities
        
        for city in cities:
            try:
                prediction = self.predictor.predict_next_aqi(city)
                if prediction:
                    trend = "↑" if prediction['change'] > 0 else "↓"
                    print(f"  {city}: {prediction['current_aqi']} → {prediction['predicted_aqi']} {trend}")
            except:
                pass
    
    def run_cycle(self):
        """Run one complete monitoring cycle"""
        print("\n" + "="*70)
        print(f"🔄 STARTING MONITORING CYCLE")
        print("="*70)
        
        # Step 1: Collect data
        self.collect_data()
        
        # Step 2: Analyze and send alerts
        self.analyze_and_alert()
        
        # Step 3: Generate predictions
        self.generate_predictions()
        
        print("\n" + "="*70)
        print("✅ CYCLE COMPLETE")
        print("="*70)
    
    def run_once(self):
        """Run the system once"""
        self.run_cycle()
        
        # Generate full report
        print("\n📋 Generating detailed report...")
        self.alert_system.generate_daily_report()
    
    def run_continuously(self, interval_minutes=60):
        """Run the system continuously"""
        print(f"\n🔄 System will run every {interval_minutes} minutes")
        print("Press Ctrl+C to stop\n")
        
        # Run immediately
        self.run_cycle()
        
        # Schedule regular runs
        schedule.every(interval_minutes).minutes.do(self.run_cycle)
        
        # Keep running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n\n🛑 System stopped by user")
            print("=" * 70)

def main():
    """Main entry point"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "AIR POLLUTION MONITORING SYSTEM" + " " * 22 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n")
    
    print("Select mode:")
    print("1. Run once with SIMULATED data (for testing)")
    print("2. Run once with REAL API data")
    print("3. Run continuously (every 60 minutes) - SIMULATED")
    print("4. Run continuously (every 60 minutes) - REAL API")
    print()
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        system = AirPollutionSystem(use_real_api=False)
        system.run_once()
    
    elif choice == "2":
        system = AirPollutionSystem(use_real_api=True)
        system.run_once()
    
    elif choice == "3":
        system = AirPollutionSystem(use_real_api=False)
        system.run_continuously(interval_minutes=60)
    
    elif choice == "4":
        system = AirPollutionSystem(use_real_api=True)
        system.run_continuously(interval_minutes=60)
    
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()