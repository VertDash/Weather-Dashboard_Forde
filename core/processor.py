class WeatherStorage:
    """
    Stores and retrieves weather data (in-memory or from disk).
    """

    def __init__(self):
        self._cache = {}

    def save(self, city: str, data: dict) -> None:
        """
        Save weather data for a city.
        """
        pass

    def load(self, city: str) -> dict:
        """
        Retrieve weather data for a city.
        """
        pass