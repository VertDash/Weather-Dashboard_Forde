import json
import os

class WeatherStorage:
    """
    This class saves weather data to a file and loading it back.
    """

    def __init__(self, filename="data/weather_data.json"):
        self.filename = filename
        # Create class and tell it where to save data
        # make sure folder exists if not, create it.
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def save(self, city: str, data: dict) -> None:
        """
        Save weather data for a specific city. takes city & data, loads 
        existing data, adds new data, and saves it all back.
        """
        all_data = {}
        # start with empty dictionary
        # Load old data first if file exists
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                try:
                    all_data = json.load(f)
                    #load existing data
                except json.JSONDecodeError:
                    all_data = {}
                    # if file is broken start fresh
        
        # add new city data 
        all_data[city] = data
        with open(self.filename, "w") as f:
            json.dump(all_data, f, indent=2)

    def load(self, city: str) -> dict:
        """
        Retrieve weather data for a city from saved file.
        """
        # see if data file exists, load data, return req city data, 
        # if no data for city returns None.
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                all_data = json.load(f)
                return all_data.get(city)
        return None