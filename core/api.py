class WeatherAPI:
    """
    Handles fetching weather data from external APIs.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_city_weather(self, city: str) -> dict:
        """
        Fetch weather data for a given city.
        """
        pass