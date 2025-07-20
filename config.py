import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from the env
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Make sure we actually get the API
if not OPENWEATHER_API_KEY:
    raise ValueError("No Openweather API key found in .env file!")