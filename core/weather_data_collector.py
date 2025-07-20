import sys
import os
import requests
import time #  add delay between retries

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import OPENWEATHER_API_KEY

print("Script started")

class WeatherDataCollector:
    """ This class gets weather data from the OpenWeather API
    
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    # Set up data collector with the API key and 'retry' settings

    def __init__(self, api_key=OPENWEATHER_API_KEY, max_retries=3, retry_delay=2):
        self.api_key = api_key
        self.max_retries = max_retries # How many times to try if it fails
        self.retry_delay = retry_delay # # How long to wait between tries

    def fetch_weather(self, city):
        """
        Get weather data for a city with error handling and retries.
        """

        # Set up the parameters for our API request
        params = {
            "q": city, # The city we want weather for
            "appid": self.api_key, # API key
            "units": "imperial" # Get temperature in Fahrenheit
        }
        attempt = 0 # Keep track of how many times tried
        while attempt < self.max_retries:
        # Make the actual request to the weather service
        # Check if we're being rate limited (too many requests)

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

                # Handling for invalid API responses. Make sure it got the 
                   # expected data
                if "main" not in data or "temp" not in data["main"]:
                    raise ValueError("Invalid API response: missing temperature data.")
                # make sure temp makes sense
                temp = data["main"]["temp"]
                if not (-100 < temp < 150):
                    raise ValueError(f"Unreasonable temperature value: {temp}")
    
                return data

            # Network issue 
            except requests.exceptions.RequestException as e:
                print(f"Network error: {e}. Retrying...")
                time.sleep(self.retry_delay)
                attempt += 1
            # data issues( invalid data, bad response etc)
            except ValueError as ve:
                print(f"Data error: {ve}")
                raise ve # dont retry for data issues

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
