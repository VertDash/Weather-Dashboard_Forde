import tkinter as tk
from tkinter import ttk
from core.weather_data_collector import WeatherDataCollector
from core.storage import WeatherStorage 
from features.city_comparison import CityComparison
from features.simple_stats import WeatherRewind


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather Gen: Now & Then")
        
        # Make window smaller and resizable
        self.geometry("900x600")
        self.minsize(700, 500)  # Minimum size
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

        # Create main container with scrollbar
        main_container = tk.Frame(self, bg="#FFFCFC")
        main_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Create canvas and scrollbar for scrolling
        canvas = tk.Canvas(main_container, bg="#FFFCFC", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FFFCFC")

        # Configure scrolling
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas_width(event):
            # Make the scrollable frame fill the canvas width
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        scrollable_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas_width)

        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel to canvas for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows/Mac
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux

        # Create notebook for tabs inside the scrollable frame
        self.notebook = ttk.Notebook(scrollable_frame)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create Current & Comparison tab
        self.current_comparison_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.current_comparison_frame, text="Current & Comparison")
        
        # City comparison feature
        self.city_comparison = CityComparison(
            self.current_comparison_frame, 
            self.collector, 
            self.storage
        )
        
        # Create Weather Rewind tab
        self.create_weather_rewind_tab()
    
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
    
    # def create_statistics_tab(self):
    #     """Placeholder for future stats tab"""
    #     stats_frame = ttk.Frame(self.notebook)
    #     self.notebook.add(stats_frame, text="Statistics")
        
    #     placeholder_label = tk.Label(
    #         stats_frame, 
    #         text="Weather Statistics\n(Coming Soon)", 
    #         font=('Arial', 16), 
    #         fg='#666666'
    #     )
    #     placeholder_label.pack(expand=True)