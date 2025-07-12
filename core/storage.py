import json
import os

class WeatherStorage:
    """
    Stores and retrieves weather data (in-memory or from disk).
    """

    def __init__(self, filename="data/weather_data.json"):
        self.filename = filename
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def save(self, city: str, data: dict) -> None:
        """
        Save weather data for a city to a JSON file.
        """
        all_data = {}
        # Load existing data if file exists
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                try:
                    all_data = json.load(f)
                except json.JSONDecodeError:
                    all_data = {}
        # Update and save
        all_data[city] = data
        with open(self.filename, "w") as f:
            json.dump(all_data, f, indent=2)

    def load(self, city: str) -> dict:
        """
        Retrieve weather data for a city from the JSON file.
        """
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                all_data = json.load(f)
                return all_data.get(city)
        return None