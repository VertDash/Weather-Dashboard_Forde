# Weather Gen: Now & Then
    A simple weather application built with Python and Tkinter that provides users with current weather data, city comparisons, historical weather insights, and inspirational daily quotes.

##  Features

### 🥵 🥶 😎 ☔️  Current Weather Display

- Real-time weather data from OpenWeatherMap API  
- Animated weather icons that pulse, drift, and flash based on weather conditions  
- Detailed weather information including temperature, humidity, wind speed, pressure  
- Sunrise and sunset times  
- Daily inspirational quotes with scrolling marquee effect  

### 🏙️ City Comparison

- Side-by-side weather comparison for two cities  
- Visual weather cards with distinct styling  
- Error handling for invalid cities and network issues  
- Save weather data locally for offline access to current weather section 

### 📊 ⏪ Weather Rewind (Historical Data)

- Last 7 days weather history in an easy-to-read table  
- 30-day weather summary with simple statistics (avg high/low, hottest/coldest days, rainy days)  
- "This Day Last Year" comparison with temperature difference analysis  
- Weather Rewind is Powered by Meteostat historical weather database  

### 🎚️ 🎛️ Enhanced User Experience

- Clean interface with tabs
- Responsive design with scrollable content  
- Color-coded weather information  
- Error handling with user-friendly messages  
- Data persistence for offline viewing  

---

## 🔧 Setup Instructions

### Prerequisites

- Python 3.7 or higher  
- OpenWeatherMap API key (free at [openweathermap.org](https://openweathermap.org))  

### Installation

1. Clone the repository:

    git clone https://github.com/your-username/Weather-Dashboard-Forde.git
    


2. Install required packages

    pip install requests python-dotenv pandas meteostat

3. Set up your API key

    Create a .env file in the root directory
    Add the following line to it:

    OPENWEATHER_API_KEY=your_api_key_here

4. Run the application
    
    python main.py

## 📖 Usage Guide

### Getting Current Weather

- Go to the "Current & Comparison" tab  
- Enter a city name in the main weather section  
- Click Get Weather to view current conditions with animated weather display  

### Comparing Cities

- In the comparison section, enter two different cities  
- Click Get Weather for each city  
- View a side-by-side comparison with detailed metrics  

### Exploring Weather History

- Switch to the "Weather Rewind" tab  
- Enter a city name and click Get Weather  
- Explore the following:
  - Last 7 Days: Daily weather summary table  
  - 30-Day Summary: Weather statistics and trends  
  - This Day Last Year: Compare current weather with exactly one year ago 




## Weather Dashboard Project Architecture
### Project Structure

```
Weather-Dashboard-Forde/
│
├── main.py                  # App entry point
├── config.py                # Loads API key from .env
├── .env                     # Stores your API key (not tracked by git)
├── .gitignore               # Tells git to ignore .env and other files
│
├── core/
│   ├── weather_data_collector.py   # Fetches weather data from API
│   ├── storage.py                  # Saves/loads weather data to file
│   ├── api.py                      # API utility functions
│   ├── processor.py                # Data processing logic
│   └── __pycache__/                # Python cache files
│
├── gui/
│   └── main_window.py              # Tkinter GUI for the app
│
├── data/
│   └── weather_data.json           # Saved weather data
│
├── features/
│   ├── city_comparison.py          # Compare weather between cities
│   ├── simple_stats.py             # Weather Rewind & statistics
│   ├── weather_icons.py            # Weather icon logic
│   ├── animated_weather_icons.py   # Animated weather icon feature
│   ├── base.py                     # Base feature class
│   └── __init__.py                 # Features package init
│
├── docs/
│   ├── Week_14_Refelction.md       # Weekly reflection
│   ├── Week_15_Reflection.md       # Weekly reflection
│   ├── Week11_Reflection.md        # Weekly reflection
│   ├── Week12_13_Reflection.md     # Weekly reflection
│
├── screenshots/
│   └── Wireframe_wk13.png          # UI wireframe/mockup
│
├── tests/
│   └── test_config.py              # Tests for config loading
│
└── README.md                       # Project overview and instructions
```
## Key Technologies
   - GUI Framework: Tkinter with custom styling

   - Weather Data: OpenWeatherMap API + Meteostat historical data

   - Data Storage: JSON-based local persistence

   - Error Handling: Comprehensive network and data validation

   - Animation: Custom Tkinter animation system

## Custom Enhancements
   - Animated Weather Icons: Custom animation system that brings weather conditions to life

   - Inspirational Quote System: Daily rotating quotes with smooth scrolling display

   - Advanced Historical Analysis: Multi-timeframe weather insights with year-over-year comparisons

   - Enhanced Error Handling: User-friendly error messages with specific guidance

   - Responsive Design: Scrollable interface that works on different screen sizes

   - Data Persistence: Smart caching system for offline functionality

## 🤝 Contributing
    The quote system incorporates inspirational content procured by multiple team members.

## 🔧 Troubleshooting
    "Invalid API key" error: Ensure your .env file contains a valid OpenWeatherMap API key

    "City not found" error: Check spelling and try using full city names

    Historical data not loading: Verify internet connection and try a major city name

    Installation issues: Ensure you have Python 3.7+ and all required packages installed
## Wireframes/BLueprints 

![App Wireframe](screenshots/Wireframe_wk13.png)