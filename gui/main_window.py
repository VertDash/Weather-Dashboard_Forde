import tkinter as tk
from tkinter import ttk
from core.weather_data_collector import WeatherDataCollector
from core.storage import WeatherStorage 
from features.city_comparison import CityComparison
from features.simple_stats import WeatherRewind


# The main window that users see and interact with
class WeatherApp(tk.Tk):
    # Initialize the parent class (tk.Tk)
    # set up window and Create all the buttons, labels, and inputs

    def __init__(self):
        super().__init__()
        self.title("Weather Dashboard")
        self.geometry("900x600")
        self.configure(bg="#FFFCFC")
        
        # Initialize data handlers
        self.collector = WeatherDataCollector()
        self.storage = WeatherStorage()
        
        self.create_widgets()

    def create_widgets(self):
        
        # Custom style for notebook tabs
        style = ttk.Style(self)
        style.theme_use('alt')
        style.configure('TNotebook.Tab', foreground='black', background='#FFFCFC')

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create Current & Comparison tab
        self.current_comparison_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.current_comparison_frame, text="Current & Comparison")
        
        # City comparison feature
        self.city_comparison = CityComparison(
            self.current_comparison_frame, 
            self.collector, 
            self.storage
        )
        
        # Placeholder for future tabs
        # Create Weather Rewind tab
        self.create_weather_rewind_tab()
        # self.create_statistics_tab()
    
    def create_weather_rewind_tab(self):
        """Create the Weather Rewind tab"""
        rewind_frame = ttk.Frame(self.notebook)
        self.notebook.add(rewind_frame, text="Weather Rewind")
        
        # Initialize Weather Rewind feature
        self.weather_rewind = WeatherRewind(
            rewind_frame,
            self.collector,
            self.storage
        )
        placeholder_label = tk.Label(
            #history_frame, 
            text="Weather History\n(Coming Soon)", 
            font=('Arial', 16), 
            fg='#666666'
        )
        placeholder_label.pack(expand=True)
    
    def create_statistics_tab(self):
        """Placeholder for future statistics tab"""
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="Statistics")
        
        placeholder_label = tk.Label(
            stats_frame, 
            text="Weather Statistics\n(Coming Soon)", 
            font=('Arial', 16), 
            fg='#666666'
        )
        placeholder_label.pack(expand=True)