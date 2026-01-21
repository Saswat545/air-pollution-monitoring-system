import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config/.env')

print("=" * 50)
print("Testing API Key Loading")
print("=" * 50)

api_key = os.getenv('OPENWEATHER_API_KEY')

print(f"API Key from .env: {api_key}")
print(f"API Key length: {len(api_key) if api_key else 0}")
print(f"Expected key: b79faaadcf36bb1ae1a6a8b94f25a11d")
print(f"Keys match: {api_key == 'b79faaadcf36bb1ae1a6a8b94f25a11d'}")

if api_key:
    print("✅ API Key is loaded!")
else:
    print("❌ API Key is NOT loaded!")
    
print("=" * 50)