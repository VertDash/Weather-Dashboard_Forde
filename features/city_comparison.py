import tkinter as tk
from features.weather_icons import get_weather_icon
from features.animated_weather_icons import AnimatedWeatherIcon


class CityComparison:
    def __init__(self, parent_frame, collector, storage):
        self.parent_frame = parent_frame
        self.collector = collector
        self.storage = storage
        
        # Store weather data for comparison
        self.weather_data = {}

        # Animation controller for main city icon
        self.main_icon_animator = None
        
        # Create the comparison interface
        self.create_comparison_interface()

        
    
    def create_comparison_interface(self):
        # Main container
        main_frame = tk.Frame(self.parent_frame, bg='#f0f0f0')
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Main Weather Section ---
        main_weather_frame = tk.Frame(main_frame, bg='#f0f0f0')
        main_weather_frame.pack(fill="x", pady=(0, 20))

        # Entry and button for main city
        tk.Label(main_weather_frame, text="Main City:", font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='black').pack(side="top", anchor="w")
        entry_frame = tk.Frame(main_weather_frame, bg='#f0f0f0')
        entry_frame.pack(fill="x", pady=(0, 10))
        self.main_city_entry = tk.Entry(entry_frame, font=('Arial', 11), width=20)
        self.main_city_entry.pack(side="left", padx=(5, 0))
        self.main_city_btn = tk.Button(entry_frame, text="Get Weather",
                                       command=self.load_main_weather,
                                       bg='#FF9800', fg='black', font=('Arial', 10, 'bold'))
        self.main_city_btn.pack(side="left", padx=(5, 0))

        # After setting up your main weather section (entry, button, etc.)
        #self.main_weather_card = self.create_weather_card(main_weather_frame, "Main City", '#FFF3E0')
        #self.main_weather_card.pack(side="left", padx=(20, 0))

        # Left: Current Weather Summary
        self.current_summary_frame = tk.Frame(main_weather_frame, bg='#E8F5E8', relief='ridge', bd=2)
        self.current_summary_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.main_icon_label = tk.Label(self.current_summary_frame, text="", font=('Arial', 48), bg='#E8F5E8')
        self.main_icon_label.pack(pady=(0, 10))


        self.city_label = tk.Label(self.current_summary_frame, text="City, State", font=('Arial', 16, 'bold'), bg='#E8F5E8', fg='black')
        self.city_label.pack(pady=(10, 5))
        self.temp_label = tk.Label(self.current_summary_frame, text="--°F", font=('Arial', 28, 'bold'), bg='#E8F5E8', fg='black')
        self.temp_label.pack()
        self.desc_label = tk.Label(self.current_summary_frame, text="Description: --", font=('Arial', 14), bg='#E8F5E8', fg='black')
        self.desc_label.pack(pady=(5, 15))

        # Right: Weather Details
        self.details_frame = tk.Frame(main_weather_frame, bg='#E3F2FD', relief='ridge', bd=2)
        self.details_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.humidity_label = tk.Label(self.details_frame, text="Humidity: --", font=('Arial', 12), bg='#E3F2FD', fg='black')
        self.humidity_label.pack(anchor="w", padx=20, pady=(10, 0))
        self.sunrise_label = tk.Label(self.details_frame, text="Sunrise: --", font=('Arial', 12), bg='#E3F2FD', fg='black')
        self.sunrise_label.pack(anchor="w", padx=20)
        self.sunset_label = tk.Label(self.details_frame, text="Sunset: --", font=('Arial', 12), bg='#E3F2FD', fg='black')
        self.sunset_label.pack(anchor="w", padx=20)
        self.windspeed_label = tk.Label(self.details_frame, text="Wind Speed: --", font=('Arial', 12), bg='#E3F2FD', fg='black')
        self.windspeed_label.pack(anchor="w", padx=20)
        self.feelslike_label = tk.Label(self.details_frame, text="Feels Like: --", font=('Arial', 12), bg='#E3F2FD', fg='black')
        self.feelslike_label.pack(anchor="w", padx=20)
        self.pressure_label = tk.Label(self.details_frame, text="Pressure: --", font=('Arial', 12), bg='#E3F2FD', fg='black')
        self.pressure_label.pack(anchor="w", padx=20)
        
        # Top section - City inputs
        input_frame = tk.Frame(main_frame, bg='#f0f0f0')
        input_frame.pack(fill="x", pady=(0, 20))
        
        # City 1 input section
        city1_frame = tk.Frame(input_frame, bg='#f0f0f0')
        city1_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        tk.Label(city1_frame, text="City 1:", font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='black').pack(anchor="w")
        self.city1_entry = tk.Entry(city1_frame, font=('Arial', 11), width=20)
        self.city1_entry.pack(fill="x", pady=(5, 0))
        self.city1_btn = tk.Button(city1_frame, text="Get Weather", 
                                  command=lambda: self.load_weather(1),
                                  bg='#4CAF50', fg='black', font=('Arial', 10, 'bold'))
        self.city1_btn.pack(pady=(5, 0))
        
        # City 2 input section
        city2_frame = tk.Frame(input_frame, bg='#f0f0f0')
        city2_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        tk.Label(city2_frame, text="City 2:", font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='black').pack(anchor="w")
        self.city2_entry = tk.Entry(city2_frame, font=('Arial', 11), width=20)
        self.city2_entry.pack(fill="x", pady=(5, 0))
        self.city2_btn = tk.Button(city2_frame, text="Get Weather", 
                                  command=lambda: self.load_weather(2),
                                  bg='#2196F3', fg='black', font=('Arial', 10, 'bold'))
        self.city2_btn.pack(pady=(5, 0))
        
        # Weather display section
        weather_frame = tk.Frame(main_frame, bg='#f0f0f0')
        weather_frame.pack(fill="both", expand=True)
        
        # City 1 weather display
        self.city1_weather_frame = self.create_weather_card(weather_frame, "City 1", '#E8F5E8')
        self.city1_weather_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # City 2 weather display
        self.city2_weather_frame = self.create_weather_card(weather_frame, "City 2", '#E3F2FD')
        self.city2_weather_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
    
    def create_weather_card(self, parent, city_label, bg_color):
        """Create a weather display card for a city"""
        # Main weather card
        card_frame = tk.Frame(parent, bg=bg_color, relief='ridge', bd=2)
        
        # City title
        title_label = tk.Label(card_frame, text=city_label, font=('Arial', 16, 'bold'), 
                              bg=bg_color, fg='#333333')
        title_label.pack(pady=(10, 5))
        
        # Weather icon
        icon_label = tk.Label(card_frame, text="", font=('Arial', 48), bg=bg_color)
        icon_label.pack(pady=(0, 10))
        card_frame.icon_label = icon_label
        
        # Temperature
        temp_label = tk.Label(card_frame, text="--°F", font=('Arial', 28, 'bold'), 
                             bg=bg_color, fg='#333333')
        temp_label.pack()
        
        # Description
        desc_label = tk.Label(card_frame, text="--", font=('Arial', 14), 
                             bg=bg_color, fg='#666666')
        desc_label.pack(pady=(5, 15))
        
        # Details frame
        details_frame = tk.Frame(card_frame, bg=bg_color)
        details_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Weather details
        feels_like_label = tk.Label(details_frame, text="Feels like: --", 
                                   font=('Arial', 10), bg=bg_color, fg='#666666')
        feels_like_label.pack(anchor="w")
        
        humidity_label = tk.Label(details_frame, text="Humidity: --", 
                                 font=('Arial', 10), bg=bg_color, fg='#666666')
        humidity_label.pack(anchor="w", pady=(2, 0))
        
        wind_label = tk.Label(details_frame, text="Wind: --", 
                             font=('Arial', 10), bg=bg_color, fg='#666666')
        wind_label.pack(anchor="w", pady=(2, 0))
        
        pressure_label = tk.Label(details_frame, text="Pressure: --", 
                                 font=('Arial', 10), bg=bg_color, fg='#666666')
        pressure_label.pack(anchor="w", pady=(2, 0))
        
        # Store references to labels for updates (icon removed for now)
        card_frame.title_label = title_label
        card_frame.icon_label = icon_label
        card_frame.temp_label = temp_label
        card_frame.desc_label = desc_label
        card_frame.feels_like_label = feels_like_label
        card_frame.humidity_label = humidity_label
        card_frame.wind_label = wind_label
        card_frame.pressure_label = pressure_label
        
        return card_frame
    
    def load_weather(self, city_number):
        """Load weather data for specified city (1 or 2)"""
        if city_number == 1:
            city = self.city1_entry.get().strip()
            weather_frame = self.city1_weather_frame
            button = self.city1_btn
        else:
            city = self.city2_entry.get().strip()
            weather_frame = self.city2_weather_frame
            button = self.city2_btn
        
        if not city:
            return
        
        # Show loading state
        button.config(text="Loading...", state='disabled')
        button.update()
        
        try:
            # Fetch weather data
            data = self.collector.fetch_weather(city)
            
            # Store data for potential future use
            self.weather_data[f'city{city_number}'] = {
                'name': city,
                'data': data
            }
            
            # Update display
            self.update_weather_display(weather_frame, city, data)
            
            # Save data
            self.storage.save(city, data)
                
        except Exception as e:
            # Show error state
            self.update_weather_display(weather_frame, city, None, str(e))
        
        finally:
            # Reset button
            button.config(text="Get Weather", state='normal')
    
    def update_weather_display(self, weather_frame, city_name, data, error=None):
        """Update weather display for a city"""
        if error:
            weather_frame.title_label.config(text=f"{city_name}")
            weather_frame.icon_label.config(text="❌")
            weather_frame.temp_label.config(text="--°F")
            weather_frame.desc_label.config(text=f"Error: {error}")
            weather_frame.feels_like_label.config(text="Feels like: --")
            weather_frame.humidity_label.config(text="Humidity: --")
            weather_frame.wind_label.config(text="Wind: --")
            weather_frame.pressure_label.config(text="Pressure: --")
            return
        
        # Update city name
        weather_frame.title_label.config(text=city_name.title())
        
        # Update weather icon (removed for now)
        weather_icon = get_weather_icon(data['weather'][0]['main'])
        weather_frame.icon_label.config(text=weather_icon)
        
        # Update temperature
        temp_f = data['main']['temp']
        weather_frame.temp_label.config(text=f"{temp_f:.0f}°F")
        
        # Update description
        description = data['weather'][0]['description'].title()
        weather_frame.desc_label.config(text=description)
        
        # Update details
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        pressure = data['main']['pressure']
        
        weather_frame.feels_like_label.config(text=f"Feels like: {feels_like:.0f}°F")
        weather_frame.humidity_label.config(text=f"Humidity: {humidity}%")
        weather_frame.wind_label.config(text=f"Wind: {wind_speed} mph")
        weather_frame.pressure_label.config(text=f"Pressure: {pressure} hPa")
    
    
    def load_main_weather(self):
        """Load weather data for main city with animated icon"""
        city = self.main_city_entry.get().strip()
        button = self.main_city_btn

        if not city:
            return
        

        # Stop any existing animation
        if self.main_icon_animator:
            self.main_icon_animator.stop_animation()
            self.main_icon_animator = None

        button.config(text="Loading...", state='disabled')
        button.update()

        try:
            data = self.collector.fetch_weather(city)

             # Start animated icon for main city
            weather_main = data['weather'][0]['main']
            self.main_icon_animator = AnimatedWeatherIcon(self.main_icon_label)
            self.main_icon_animator.start_animation(weather_main)

            # Update icon
            #weather_icon = get_weather_icon(data['weather'][0]['main'])
            #self.main_icon_label.config(text=weather_icon)
            
            # Update summary
            self.city_label.config(text=city.title())
            self.temp_label.config(text=f"{data['main']['temp']:.0f}°F")
            self.desc_label.config(text=data['weather'][0]['description'].title())
            # Update details
            self.humidity_label.config(text=f"Humidity: {data['main']['humidity']}%")
            self.sunrise_label.config(text=f"Sunrise: {self.format_time(data['sys']['sunrise'])}")
            self.sunset_label.config(text=f"Sunset: {self.format_time(data['sys']['sunset'])}")
            self.windspeed_label.config(text=f"Wind Speed: {data['wind']['speed']} mph")
            self.feelslike_label.config(text=f"Feels Like: {data['main']['feels_like']:.0f}°F")
            self.pressure_label.config(text=f"Pressure: {data['main']['pressure']} hPa")
            self.storage.save(city, data)
        except Exception as e:
            # Stop animation on error
            if self.main_icon_animator:
                self.main_icon_animator.stop_animation()
                self.main_icon_animator = None

            self.main_icon_label.config(text="❌")
            self.city_label.config(text=city.title())
            self.temp_label.config(text="--°F")
            self.desc_label.config(text=f"Error: {e}")
            self.humidity_label.config(text="Humidity: --")
            self.sunrise_label.config(text="Sunrise: --")
            self.sunset_label.config(text="Sunset: --")
            self.windspeed_label.config(text="Wind Speed: --")
            self.feelslike_label.config(text="Feels Like: --")
            self.pressure_label.config(text="Pressure: --")
        finally:
            button.config(text="Get Weather", state='normal')

    def format_time(self, timestamp):
        import datetime
        return datetime.datetime.fromtimestamp(timestamp).strftime('%I:%M %p')
    
    def __del__(self):
        """Cleanup animations when object is destroyed"""
        if self.main_icon_animator:
            self.main_icon_animator.stop_animation()