import sys
import os
import requests
import time 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import OPENWEATHER_API_KEY

print("Script started")

class WeatherDataCollector:
    """
    Collects weather data from OpenWeatherMap API with robust error handling and data validation.
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key=OPENWEATHER_API_KEY, max_retries=3, retry_delay=2):
        self.api_key = api_key
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def fetch_weather(self, city):
        """
        Fetch weather data for a given city with error handling and validation.
        Returns a dict with weather data or raises an exception.
        """
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "imperial"
        }
        attempt = 0
        while attempt < self.max_retries:
            try:
                response = requests.get(self.BASE_URL, params=params, timeout=5)
                
                # Rate limit handling
                if response.status_code == 429:
                    print("Rate limit exceeded. Retrying...")
                    time.sleep(self.retry_delay)
                    attempt += 1
                    continue
                # Handle for invalid city 
                if response.status_code == 404:
                    data = response.json()
                    if data.get("message", "").lower() == "city not found":
                        raise ValueError("Invalid city name.")
                
                response.raise_for_status()
                data = response.json()

                # Handling for invalid API responses
                if "main" not in data or "temp" not in data["main"]:
                    raise ValueError("Invalid API response: missing temperature data.")

                temp = data["main"]["temp"]
                if not (-100 < temp < 150):
                    raise ValueError(f"Unreasonable temperature value: {temp}")
    
                return data

            except requests.exceptions.RequestException as e:
                print(f"Network error: {e}. Retrying...")
                time.sleep(self.retry_delay)
                attempt += 1
            except ValueError as ve:
                print(f"Data error: {ve}")
                raise ve

        raise Exception("Failed to fetch weather data after multiple attempts.")

# --- Example Test Cases ---

def test_valid_city():
    collector = WeatherDataCollector()
    try:
        data = collector.fetch_weather("Boston")
        print("Test valid city: PASS")
    except Exception as e:
        print(f"Test valid city: FAIL ({e})")

def test_invalid_city():
    collector = WeatherDataCollector()
    try:
        collector.fetch_weather("NotARealCity123")
        print("Test invalid city: FAIL (should have raised)")
    except Exception as e:
        print(f"Test invalid city: PASS ({e})")

def test_rate_limit():
    # Simulate by manually setting status_code to 429 in a mock, or just describe:
    print("Test rate limit: Simulate by mocking requests to return 429.")

def test_unreasonable_temp():
    # Simulate by mocking API response with bad temp, or just describe:
    print("Test unreasonable temp: Simulate by mocking API response with temp=9999.")

if __name__ == "__main__":
    test_valid_city()
    test_invalid_city()
    test_rate_limit()
    test_unreasonable_temp()

"""
# Documentation of Error Scenarios Handled

1. **Network connectivity issues:**  
   - Caught with `requests.exceptions.RequestException`
   - Retries up to `max_retries` times with a delay

2. **Invalid API responses:**  
   - Checks if expected keys are present in the response
   - Raises ValueError if data is missing or malformed

3. **Rate limiting:**  
   - Checks for HTTP 429 status code
   - Waits and retries if rate limit is hit

4. **Data validation:**  
   - Ensures temperature is within a reasonable range (-100 to 150 F)
   - Raises ValueError if data is out of bounds

# Extension
To support multiple weather APIs, you could:
- Add a method for each API and select based on config
- Use a base class/interface for API collectors
- Standardize data format in a post-processing step
"""