def get_weather_icon(weather_main):
    """Return an emoji icon for a given OpenWeatherMap 'main' weather string."""
    icons = {
        'Clear': '☀️',
        'Clouds': '☁️',
        'Rain': '🌧️',
        'Drizzle': '🌦️',
        'Thunderstorm': '⛈️',
        'Snow': '🌨️',
        'Mist': '🌫️',
        'Fog': '🌫️',
        'Haze': '🌫️'
    }
    return icons.get(weather_main, '🌤️')