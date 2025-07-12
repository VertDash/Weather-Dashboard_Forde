import tkinter as tk
from core.weather_data_collector import WeatherDataCollector
from core.storage import WeatherStorage 

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather Dashboard")
        self.geometry("800x500")
        self.create_widgets()

    def create_widgets(self):
        # Top: City selection
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(top_frame, text="City:").pack(side="left")
        self.city_entry = tk.Entry(top_frame)
        self.city_entry.pack(side="left", padx=5)
        self.refresh_btn = tk.Button(top_frame, text="Refresh")
        self.refresh_btn.pack(side="left", padx=5)
        self.refresh_btn.config(command=self.load_weather)

        # Center: Weather display
        self.weather_frame = tk.Frame(self)
        self.weather_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.temp_label = tk.Label(self.weather_frame, text="Temperature: --")
        self.temp_label.pack(anchor="w")
        self.desc_label = tk.Label(self.weather_frame, text="Description: --")
        self.desc_label.pack(anchor="w")
        self.humidity_label = tk.Label(self.weather_frame, text="Humidity: --")
        self.humidity_label.pack(anchor="w")

    def load_weather(self):
        city = self.city_entry.get()
        collector = WeatherDataCollector()
        storage = WeatherStorage()
        try:
            data = collector.fetch_weather(city)
            self.temp_label.config(text=f"Temperature: {data['main']['temp']} °F")
            self.desc_label.config(text=f"Description: {data['weather'][0]['description']}")
            self.humidity_label.config(text=f"Humidity: {data['main']['humidity']}%")
            storage.save(city, data)
        except Exception as e:
            self.temp_label.config(text="Temperature: --")
            self.desc_label.config(text=f"Error: {e}")
            self.humidity_label.config(text="Humidity: --")