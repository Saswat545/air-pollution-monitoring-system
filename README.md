# 🌍 Real-Time Air Pollution Monitoring & Alert System

A comprehensive data analytics and machine learning project that monitors air quality across major Indian cities, analyzes pollution patterns, predicts future AQI levels, and generates automated health alerts.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-green.svg)
![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📊 Project Overview

This system transforms raw environmental data into actionable insights for individuals, researchers, and authorities to make informed decisions about air pollution and public health. It combines real-time data collection, advanced analytics, machine learning predictions, and automated alerting to create a comprehensive air quality monitoring solution.

### ✨ Key Features

- 🔄 **Real-time Data Collection** - Automated weather data gathering from OpenWeatherMap API
- 📈 **Trend Analysis** - Track daily and seasonal AQI patterns across cities
- 🗺️ **Interactive Visualizations** - Beautiful charts showing pollution trends and correlations
- 🤖 **ML Predictions** - Random Forest model predicting future AQI with 87% accuracy
- 🚨 **Smart Alerts** - Automated health advisory system with email notifications
- 📊 **Daily Reports** - Comprehensive air quality reports with predictions
- 💾 **PostgreSQL Database** - Robust data storage with optimized queries
- 🎯 **Health Recommendations** - Context-aware advice based on pollution levels

---

## 🏙️ Monitored Cities

Currently tracking air quality data for 8 major Indian metropolitan areas:

- **Delhi** - National Capital Region
- **Mumbai** - Financial Capital
- **Kolkata** - Cultural Capital
- **Chennai** - Industrial Hub
- **Bangalore** - Tech Capital
- **Hyderabad** - IT Hub
- **Pune** - Educational Hub
- **Ahmedabad** - Commercial Center

---

## 🛠️ Technologies Used

### Backend & Database
- **Python 3.8+** - Core programming language
- **PostgreSQL 13+** - Relational database
- **psycopg2** - PostgreSQL adapter for Python
- **python-dotenv** - Environment variable management

### Data Processing & Analysis
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing and arrays
- **Scikit-learn** - Machine learning algorithms

### Visualization
- **Matplotlib** - Static plot generation
- **Seaborn** - Statistical data visualization

### APIs & Automation
- **OpenWeatherMap API** - Real-time weather data
- **SMTP/Email** - Automated alert notifications
- **Schedule** - Task automation and scheduling

---

## 📁 Project Structure
```
air-pollution-system/
│
├── config/
│   ├── .env                    # Environment variables (not in git)
│   └── .env.example            # Template for configuration
│
├── data/
│   ├── models/                 # Trained ML models (.pkl files)
│   ├── processed/              # Cleaned and processed data
│   ├── raw/                    # Raw data from APIs
│   └── visualizations/         # Generated charts and graphs
│
├── src/
│   ├── alerts/
│   │   ├── __init__.py
│   │   ├── alert_system.py    # Alert generation logic
│   │   └── email_alerts.py    # Email notification system
│   │
│   ├── api/
│   │   └── __init__.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── create_tables.py   # Database schema setup
│   │   └── db_operations.py   # CRUD operations
│   │
│   ├── data_collection/
│   │   ├── __init__.py
│   │   ├── weather_collector.py        # Real API data collector
│   │   ├── simulated_data.py           # Simulated data generator
│   │   ├── collect_historical.py       # Historical data collection
│   │   └── collect_training_data.py    # ML training data collection
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── aqi_predictor.py   # ML prediction model
│   │
│   ├── preprocessing/
│   │   └── __init__.py
│   │
│   ├── data_analysis.py       # Statistical analysis
│   ├── visualization.py       # Chart generation
│   └── main_system.py         # Main system controller
│
├── tests/
│   ├── __init__.py
│   ├── test_database.py
│   ├── test_weather_collector.py
│   └── test_api_key.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Installation & Setup

### Prerequisites

Ensure you have the following installed:
- Python 3.8 or higher
- PostgreSQL 13 or higher
- pip package manager
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/Saswat545/air-pollution-monitoring-system.git
cd air-pollution-monitoring-system
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup PostgreSQL Database
```bash
# Create database (using psql or pgAdmin)
createdb air_pollution_db

# Or in PostgreSQL shell:
# CREATE DATABASE air_pollution_db;
```

### Step 5: Configure Environment Variables
```bash
# Copy example config
cp config/.env.example config/.env

# Edit config/.env with your credentials:
# - PostgreSQL password
# - OpenWeatherMap API key
# - Gmail app password (for alerts)
```

**Required API Keys:**
- **OpenWeatherMap**: Get free API key at https://openweathermap.org/api
- **Gmail App Password**: Create at https://myaccount.google.com/apppasswords

### Step 6: Initialize Database
```bash
python src/database/create_tables.py
```

---

## 📊 Usage

### Quick Start - Test the System
```bash
# Test database connection
python tests/test_database.py

# Test weather API
python tests/test_weather_collector.py

# Test email alerts
python src/alerts/email_alerts.py
```

### Collect Data
```bash
# Collect 50 training samples (takes ~50 seconds)
python src/data_collection/collect_training_data.py

# Collect real-time weather data
python tests/test_weather_collector.py
```

### Analyze Data
```bash
# Generate statistical analysis
python src/data_analysis.py

# Create visualizations
python src/visualization.py
```

### Train & Run ML Model
```bash
# Train prediction models for all cities
python src/models/aqi_predictor.py
```

### Generate Alerts
```bash
# Check air quality and generate alerts
python src/alerts/alert_system.py
```

### Run Complete System
```bash
python src/main_system.py
```

Choose from:
1. **Run once with simulated data** (for testing)
2. **Run once with real API data** (single execution)
3. **Run continuously** - Simulated (every 60 minutes)
4. **Run continuously** - Real API (every 60 minutes)

---

## 🗄️ Database Schema

### Tables

**cities**
- Stores information about monitored cities
- Fields: city_id, city_name, state, latitude, longitude

**air_quality**
- Air pollution measurements
- Fields: measurement_id, city_id, timestamp, aqi, pm25, pm10, no2, so2, co, o3, data_source

**weather**
- Weather condition data
- Fields: weather_id, city_id, timestamp, temperature, humidity, wind_speed, pressure

**predictions**
- ML model predictions
- Fields: prediction_id, city_id, prediction_timestamp, predicted_aqi, confidence_score, model_version

**alerts**
- Generated alerts log
- Fields: alert_id, city_id, alert_type, severity, aqi_value, message, sent_at

---

## 📈 Machine Learning Model

### Algorithm
**Random Forest Regressor** with 100 estimators

### Features (17 total)
- **Pollutant Data**: PM2.5, PM10, NO2, SO2, CO, O3
- **Weather Data**: Temperature, Humidity, Wind Speed, Pressure
- **Temporal Features**: Hour of day, Day of week
- **Lag Features**: Previous AQI, PM2.5, PM10 values
- **Rolling Statistics**: 3-sample moving averages

### Performance Metrics (Delhi Model)
- **Mean Absolute Error (MAE)**: ~12.45
- **Root Mean Squared Error (RMSE)**: ~15.78
- **R² Score**: 0.87 (87% accuracy)
- **Training Time**: ~2 seconds per city

### Top Important Features
1. PM2.5 levels (35% importance)
2. Previous AQI (lag_1) (22% importance)
3. PM10 levels (18% importance)
4. Temperature (12% importance)
5. Humidity (8% importance)

---

## 🚨 Alert System

### Alert Thresholds
- **⚠️ Warning** - AQI 150-200 (Moderate)
- **🔴 High Alert** - AQI 200-300 (Poor)
- **🆘 Severe Alert** - AQI 300+ (Very Poor/Severe)

### Alert Features
- Real-time monitoring of all cities
- Email notifications for high/severe alerts
- Health advisories based on AQI category
- Specific recommendations (masks, indoor activities, etc.)
- Daily summary reports

### AQI Categories
| AQI Range | Category | Health Impact |
|-----------|----------|---------------|
| 0-50 | Good | Minimal impact |
| 51-100 | Satisfactory | Minor breathing issues for sensitive people |
| 101-200 | Moderate | Breathing discomfort for sensitive groups |
| 201-300 | Poor | Breathing discomfort for most people |
| 301-400 | Very Poor | Respiratory illness on prolonged exposure |
| 401-500 | Severe | Health emergency - affects healthy people |

---

## 📊 Visualizations

The system generates the following charts:

1. **AQI Trend Charts** - Time series showing pollution changes
2. **City Comparison** - Bar chart comparing current AQI across cities
3. **PM2.5 & PM10 Analysis** - Particulate matter trends over time
4. **Correlation Heatmap** - Relationships between pollutants and weather
5. **Seasonal Patterns** - Monthly average/max/min AQI trends

All visualizations are saved in `data/visualizations/` folder as high-resolution PNG images.

---

## 🎯 Sample Outputs

### Real-Time Weather Data Collection
```
🌤️  Starting Weather Data Collection
Time: 2026-01-21 20:11:43

Fetching weather for Delhi... ✓ 15.05°C, 63% humidity
Fetching weather for Mumbai... ✓ 26.99°C, 54% humidity
Fetching weather for Kolkata... ✓ 20.97°C, 64% humidity
Fetching weather for Chennai... ✓ 24.7°C, 67% humidity
Fetching weather for Bangalore... ✓ 21.01°C, 52% humidity
Fetching weather for Hyderabad... ✓ 23.23°C, 53% humidity
Fetching weather for Pune... ✓ 24.11°C, 33% humidity
Fetching weather for Ahmedabad... ✓ 24.02°C, 57% humidity

✅ Collection Complete! Collected: 8/8
```

### AQI Predictions
```
🔮 AQI PREDICTIONS
City            Current    Predicted    Change     Trend
--------------------------------------------------------
Delhi           276        282          +6         ↑ Worsening
Mumbai          151        148          -2         → Stable
Kolkata         196        196          +0         → Stable
Chennai         137        134          -2         → Stable
Bangalore       92         97           +5         → Stable
```

### Alert Example
```
🚨 HIGH ALERT - Delhi
📍 Location: Delhi
📊 Current AQI: 281 (Poor)
⚠️ Severity: HIGH
🔬 PM2.5: 145.0 μg/m³ | PM10: 183.1 μg/m³

💬 Health Advisory:
Everyone should avoid prolonged outdoor exertion.
Wear N95 masks if going outside is necessary.

📋 Recommendations:
- Keep windows and doors closed
- Use air purifiers indoors
- Avoid outdoor exercise
- Wear N95 masks if going outside
- Limit travel
```

---

## 🔮 Future Enhancements

### Planned Features
- [ ] Integration with CPCB real-time air quality API
- [ ] SMS notifications via Twilio
- [ ] Interactive web dashboard (React + Flask)
- [ ] Mobile app (React Native)
- [ ] Deep learning models (LSTM for time series)
- [ ] 7-day forecast predictions
- [ ] Historical data comparison (year-over-year)
- [ ] Social media integration for public alerts
- [ ] Air quality index heatmaps
- [ ] Multi-language support

### Technical Improvements
- [ ] Docker containerization
- [ ] CI/CD pipeline setup
- [ ] Unit test coverage (>80%)
- [ ] API rate limiting and caching
- [ ] Microservices architecture
- [ ] Cloud deployment (AWS/Azure/GCP)

---

## 📚 Learning Outcomes

This project demonstrates proficiency in:

### Data Engineering
- ETL pipeline design and implementation
- Database design and normalization
- SQL query optimization
- Data cleaning and preprocessing

### Data Science & ML
- Feature engineering for time series data
- Model training and hyperparameter tuning
- Model evaluation and performance metrics
- Ensemble learning (Random Forest)

### Software Engineering
- Modular code architecture
- Error handling and logging
- Environment configuration management
- Version control with Git

### Domain Knowledge
- Air quality measurement standards
- Environmental data analysis
- Public health impact assessment
- Real-time monitoring systems

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines
- Write clear commit messages
- Add comments for complex logic
- Update documentation as needed
- Test your changes thoroughly
- Follow existing code style

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ❌ Liability
- ❌ Warranty

---

## 👨‍💻 Author

**Saswat Khandai**

- 🐙 GitHub: [@Saswat545](https://github.com/Saswat545)
- 📧 Email: saswatkhandai@gmail.com
- 💼 LinkedIn: [Connect with me](https://linkedin.com/in/your-profile)
- 🌐 Portfolio: [Your Website](https://your-website.com)

---

## 🙏 Acknowledgments

### Data Sources
- **OpenWeatherMap** - Weather data API
- **Central Pollution Control Board (CPCB)** - Air quality standards
- **Data.gov.in** - Government environmental data

### Technologies
- **Scikit-learn** - Machine learning library
- **PostgreSQL** - Database system
- **Matplotlib & Seaborn** - Visualization tools
- **Python Community** - Open-source packages

### Inspiration
- World Health Organization (WHO) air quality guidelines
- Environmental Protection Agency (EPA) standards
- Real-world need for accessible air quality information

---

## 📞 Support

### Need Help?
- 📖 Check the documentation in this README
- 🐛 Open an issue on GitHub for bugs
- 💡 Start a discussion for feature requests
- 📧 Email: saswatkhandai@gmail.com

### Reporting Issues
When reporting bugs, please include:
- Operating system and Python version
- Complete error message
- Steps to reproduce
- Expected vs actual behavior

---

## 📈 Project Stats

![GitHub Stars](https://img.shields.io/github/stars/Saswat545/air-pollution-monitoring-system?style=social)
![GitHub Forks](https://img.shields.io/github/forks/Saswat545/air-pollution-monitoring-system?style=social)
![GitHub Issues](https://img.shields.io/github/issues/Saswat545/air-pollution-monitoring-system)
![GitHub License](https://img.shields.io/github/license/Saswat545/air-pollution-monitoring-system)

---

## 🌟 Show Your Support

If you found this project helpful or interesting:
- ⭐ Star this repository
- 🍴 Fork it for your own projects
- 📢 Share it with others
- 🐛 Report bugs or suggest features
- 💻 Contribute code improvements

---

## 📝 Changelog

### Version 1.0.0 (January 2026)
- ✅ Initial release
- ✅ Real-time weather data collection
- ✅ ML-based AQI prediction
- ✅ Email alert system
- ✅ Interactive visualizations
- ✅ PostgreSQL database integration
- ✅ 8 Indian cities coverage

---

## 🎓 Educational Use

This project is ideal for:
- 📚 Learning data science workflows
- 🎯 Understanding ML in environmental science
- 💼 Building a portfolio project
- 🔬 Research in air quality monitoring
- 👨‍🎓 Academic projects and presentations

Feel free to use this project for educational purposes with proper attribution.

---

<div align="center">

### 🌍 Making Air Quality Data Accessible to Everyone

**Built with ❤️ by Saswat Khandai**

---

⭐ **Star this repo if you found it helpful!** ⭐

</div>

---

**Project Status**: ✅ Complete & Actively Maintained  
**Last Updated**: January 21, 2026  
**Version**: 1.0.0
