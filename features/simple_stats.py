import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import requests
import pandas as pd
from meteostat import Point, Daily

class WeatherRewind:
    def __init__(self, parent_frame, collector, storage):
        self.parent_frame = parent_frame
        self.collector = collector
        self.storage = storage
        
        # Store data for the interface
        self.location_coords = None
        self.current_city = None
        
        self.create_rewind_interface()
    
    def create_rewind_interface(self):
        """Create the Weather Rewind interface matching your wireframe"""
        # Main container
        main_frame = tk.Frame(self.parent_frame, bg='#FFFCFC')
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="Weather Rewind", 
                              font=('Arial', 18, 'bold'), bg='#FFFCFC', fg='black')
        title_label.pack(pady=(0, 20))
        
        # Location input section
        location_frame = tk.LabelFrame(main_frame, text="Location", 
                                     font=('Arial', 12, 'bold'), bg='#FFFCFC', 
                                     fg='black', relief='ridge', bd=2)
        location_frame.pack(fill="x", pady=(0, 20))
        
        input_frame = tk.Frame(location_frame, bg='#FFFCFC')
        input_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(input_frame, text="City:", font=('Arial', 12, 'bold'), 
                bg='#FFFCFC', fg='black').pack(side="left")
        
        self.city_entry = tk.Entry(input_frame, font=('Arial', 11), width=30)
        self.city_entry.pack(side="left", padx=(10, 10), fill="x", expand=True)
        
        self.get_weather_btn = tk.Button(input_frame, text="Get Weather",
                                       command=self.load_historical_data,
                                       bg='#4CAF50', fg='black', font=('Arial', 10, 'bold'))
        self.get_weather_btn.pack(side="right", padx=(10, 0))
        
        # Content area with three sections
        content_frame = tk.Frame(main_frame, bg='#FFFCFC')
        content_frame.pack(fill="both", expand=True)
        
        # Last 7 Days section
        self.create_last_7_days_section(content_frame)
        
        # Last 30 Days Summary section  
        self.create_30_day_summary_section(content_frame)
        
        # This Day Last Year section
        self.create_this_day_last_year_section(content_frame)
    
    def create_last_7_days_section(self, parent):
        """Create the Last 7 Days table section"""
        # Frame for Last 7 Days
        last_7_frame = tk.LabelFrame(parent, text="Last 7 Days", 
                                   font=('Arial', 12, 'bold'), bg='#FFFCFC', 
                                   fg='black', relief='ridge', bd=2)
        last_7_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Create table with headers
        table_frame = tk.Frame(last_7_frame, bg='white', relief='sunken', bd=1)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Headers
        headers = ["Date", "Temp", "Description"]
        header_colors = ['#e0e0e0', '#e0e0e0', '#e0e0e0']
        
        for i, (header, color) in enumerate(zip(headers, header_colors)):
            header_label = tk.Label(table_frame, text=header, font=('Arial', 11, 'bold'),
                                  bg=color, relief='ridge', bd=1)
            header_label.grid(row=0, column=i, sticky="ew", ipadx=10, ipady=5)
        
        # Configure grid weights
        for i in range(3):
            table_frame.grid_columnconfigure(i, weight=1)
        
        # Store reference for data rows
        self.last_7_table = table_frame
        self.last_7_rows = []
        
        # Create 7 data rows
        for row_idx in range(1, 8):
            row_data = []
            for col in range(3):
                cell = tk.Label(table_frame, text="--", font=('Arial', 10),
                              bg='white', fg='black', relief='ridge', bd=1)
                cell.grid(row=row_idx, column=col, sticky="ew", ipadx=10, ipady=3)
                row_data.append(cell)
            self.last_7_rows.append(row_data)
    
    def create_30_day_summary_section(self, parent):
        """Create the Last 30 Days Summary section"""
        summary_frame = tk.LabelFrame(parent, text="Last 30 Days Summary",
                                    font=('Arial', 12, 'bold'), bg='#FFFCFC',
                                    fg='black', relief='ridge', bd=2)
        summary_frame.pack(side="left", fill="both", expand=True, padx=(5, 5))
        
        # Summary statistics
        stats_frame = tk.Frame(summary_frame, bg='#FFFCFC')
        stats_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Create labels for each statistic
        stats_data = [
            ("Average High:", "76°F"),
            ("Average Low:", "62°F"),
            ("Hottest Day:", "85°F"),
            ("Coldest Day:", "55°F"),
            ("Most Common:", "Sunny"),
            ("Rainy Days:", "8 days")
        ]
        
        self.summary_labels = {}
        for i, (label_text, default_value) in enumerate(stats_data):
            # Create frame for each row
            row_frame = tk.Frame(stats_frame, bg='#FFFCFC')
            row_frame.pack(fill="x", pady=3)
            
            # Label on left
            tk.Label(row_frame, text=label_text, font=('Arial', 11), 
                    bg='#FFFCFC', fg='black').pack(side="left")
            
            # Value on right
            value_label = tk.Label(row_frame, text=default_value, font=('Arial', 11), 
                                 bg='#FFFCFC', fg='black')
            value_label.pack(side="right")
            
            # Store references
            key = label_text.lower().replace(' ', '_').replace(':', '')
            self.summary_labels[key] = value_label
    
    def create_this_day_last_year_section(self, parent):
        """Create the This Day Last Year section"""
        last_year_frame = tk.LabelFrame(parent, text="This Day Last Year",
                                      font=('Arial', 12, 'bold'), bg='#FFFCFC',
                                      fg='black', relief='ridge', bd=2)
        last_year_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        content_frame = tk.Frame(last_year_frame, bg='#FFFCFC')
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Date display
        self.last_year_date_label = tk.Label(content_frame, text="July 25, 2024",
                                           font=('Arial', 14, 'bold'), bg='#FFFCFC', fg='black')
        self.last_year_date_label.pack(pady=(10, 15))
        
        # Temperature display
        self.last_year_temp_label = tk.Label(content_frame, text="82°F",
                                           font=('Arial', 32, 'bold'), bg='#FFFCFC', fg='black')
        self.last_year_temp_label.pack(pady=(0, 10))
        
        # Weather description
        self.last_year_desc_label = tk.Label(content_frame, text="Sunny",
                                           font=('Arial', 12), bg='#FFFCFC', fg='black')
        self.last_year_desc_label.pack(pady=(0, 20))
        
        # Comparison with today
        self.comparison_label = tk.Label(content_frame, text="vs Today: 10°F Cooler",
                                       font=('Arial', 11), bg='#FFFCFC', fg='blue')
        self.comparison_label.pack()
    
    def get_coordinates_from_city(self, city_name):
        """Get latitude and longitude for a city using OpenWeatherMap geocoding"""
        try:
            geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
            params = {
                "q": city_name,
                "limit": 1,
                "appid": self.collector.api_key
            }
            
            response = requests.get(geocoding_url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
            else:
                raise ValueError("City not found")
                
        except Exception as e:
            raise Exception(f"Failed to get coordinates: {e}")
    
    def load_historical_data(self):
        """Load and display historical weather data"""
        city = self.city_entry.get().strip()
        if not city:
            return
        
        # Show loading state
        self.get_weather_btn.config(text="Loading...", state='disabled')
        self.get_weather_btn.update()
        
        try:
            # Get coordinates for the city
            lat, lon = self.get_coordinates_from_city(city)
            self.location_coords = Point(lat, lon)
            self.current_city = city
            
            # Load different time periods
            self.load_7_day_data()
            self.load_30_day_summary()
            self.load_this_day_last_year()
            
        except Exception as e:
            self.show_error(str(e))
            
        finally:
            self.get_weather_btn.config(text="Get Weather", state='normal')
    
    def load_7_day_data(self):
        """Load and display 7-day weather data"""
        print("Starting to load 7-day data...")
        print(f"Location coordinates: {self.location_coords}")
        
        try:
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = today
            start_date = end_date - timedelta(days=6)
            
            print(f"Date range: {start_date} to {end_date}")
            
            data = Daily(self.location_coords, start_date, end_date)
            df = data.fetch()
            
            print(f"Raw DataFrame shape: {df.shape}")
            print(f"DataFrame columns: {df.columns.tolist()}")
            print(f"DataFrame index: {df.index.tolist()}")
            
            if df.empty:
                raise ValueError("No historical data available")

            self.weather_data = []

            for date, row in df.iterrows():
                print(f"Processing date: {date}")
                print(f"Raw row data: {row.to_dict()}")
                
                # Safely handle missing values using pd.isna()
                tavg = row['tavg'] if not pd.isna(row['tavg']) else None
                tmax = row['tmax'] if not pd.isna(row['tmax']) else None
                tmin = row['tmin'] if not pd.isna(row['tmin']) else None
                prcp = row['prcp'] if not pd.isna(row['prcp']) else 0
                snow = row['snow'] if not pd.isna(row['snow']) else 0

                day_data = {
                    'date': date.strftime('%Y-%m-%d'),
                    'tavg': tavg,
                    'tmax': tmax,
                    'tmin': tmin,
                    'prcp': prcp,
                    'snow': snow
                }

                # Get human-readable weather description
                weather_desc = self.get_weather_description_simple(day_data)
                day_data['description'] = weather_desc
                
                print(f"Processed day_data: {day_data}")
                self.weather_data.append(day_data)

            # Sort data by date (newest first for display)
            self.weather_data.sort(key=lambda x: x['date'], reverse=True)
            
            print(f"Successfully loaded {len(self.weather_data)} days of data")
            print("Weather data summary:")
            for i, day in enumerate(self.weather_data):
                print(f"  Day {i}: {day['date']} - {day['description']}")
            
            self.loaded = True
            self.display_weather_table()

        except Exception as e:
            print(f"Error loading 7-day data: {e}")
            import traceback
            traceback.print_exc()
            self.weather_data = []
            self.loaded = False
            # Make sure to still call display_weather_table to show empty data
            self.display_weather_table()
           

    def display_weather_table(self):
        """Update the 7-day table with loaded weather data."""
        print(f"Displaying weather table with {len(self.weather_data)} items")
        
        for i, row_widgets in enumerate(self.last_7_rows):
            print(f"Processing table row {i}")
            
            if i < len(self.weather_data):
                day_data = self.weather_data[i]
                print(f"  Using data: {day_data}")
                
                # Format date - data is now sorted newest first
                if i == 0:
                    date_str = "Today"
                elif i == 1:
                    date_str = "Yesterday"
                else:
                    try:
                        date_obj = datetime.strptime(day_data['date'], "%Y-%m-%d")
                        date_str = date_obj.strftime("%b %d")
                    except Exception as e:
                        print(f"  Date parsing error: {e}")
                        date_str = day_data['date']
                
                # Get temperature
                temp_c = day_data['tavg'] if day_data['tavg'] is not None else day_data['tmax']
                temp_f = (temp_c * 9/5) + 32 if temp_c is not None else None
                description = day_data.get('description', "--")
                
                # Update the cells
                temp_text = f"{temp_f:.0f}°F" if temp_f else "--°F"
                
                print(f"  Setting: {date_str}, {temp_text}, {description}")
                
                row_widgets[0].config(text=date_str)
                row_widgets[1].config(text=temp_text)
                row_widgets[2].config(text=description)
                
                # Force update
                row_widgets[0].update()
                row_widgets[1].update()
                row_widgets[2].update()
                
            else:
                print(f"  No data for row {i}, clearing")
                row_widgets[0].config(text="--")
                row_widgets[1].config(text="--°F")
                row_widgets[2].config(text="--")
        
        print("Table update complete")

    def load_30_day_summary(self):
        """Load and display 30-day summary statistics"""
        try:
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = today
            start_date = end_date - timedelta(days=29)
            
            data = Daily(self.location_coords, start_date, end_date)
            df = data.fetch()
            
            if df.empty:
                raise ValueError("No historical data available")
            
            # Convert to simple data structures and calculate manually
            temps_high = []
            temps_low = []
            rainy_days = 0
            weather_types = {"Sunny": 0, "Rainy": 0, "Cloudy": 0, "Snowy": 0}
            
            for date, row in df.iterrows():
                # Collect temperatures
                if not pd.isna(row['tmax']):
                    temps_high.append(row['tmax'])
                if not pd.isna(row['tmin']):
                    temps_low.append(row['tmin'])
                
                # Count rainy days
                if not pd.isna(row['prcp']) and row['prcp'] > 0:
                    rainy_days += 1
                
                # Count weather types
                day_data = {
                    'tavg': row['tavg'] if not pd.isna(row['tavg']) else None,
                    'tmax': row['tmax'] if not pd.isna(row['tmax']) else None,
                    'prcp': row['prcp'] if not pd.isna(row['prcp']) else 0,
                    'snow': row['snow'] if not pd.isna(row['snow']) else 0
                }
                weather_desc = self.get_weather_description_simple(day_data)
                if weather_desc in weather_types:
                    weather_types[weather_desc] += 1
            
            # Calculate averages manually
            avg_high_c = sum(temps_high) / len(temps_high) if temps_high else None
            avg_low_c = sum(temps_low) / len(temps_low) if temps_low else None
            hottest_c = max(temps_high) if temps_high else None
            coldest_c = min(temps_low) if temps_low else None
            
            # Convert to Fahrenheit
            avg_high_f = (avg_high_c * 9/5) + 32 if avg_high_c is not None else None
            avg_low_f = (avg_low_c * 9/5) + 32 if avg_low_c is not None else None
            hottest_f = (hottest_c * 9/5) + 32 if hottest_c is not None else None
            coldest_f = (coldest_c * 9/5) + 32 if coldest_c is not None else None
            
            # Find most common weather
            most_common = max(weather_types, key=weather_types.get) if any(weather_types.values()) else "Sunny"
            
            # Update labels
            self.summary_labels['average_high'].config(
                text=f"{avg_high_f:.0f}°F" if avg_high_f is not None else "--°F")
            self.summary_labels['average_low'].config(
                text=f"{avg_low_f:.0f}°F" if avg_low_f is not None else "--°F")
            self.summary_labels['hottest_day'].config(
                text=f"{hottest_f:.0f}°F" if hottest_f is not None else "--°F")
            self.summary_labels['coldest_day'].config(
                text=f"{coldest_f:.0f}°F" if coldest_f is not None else "--°F")
            self.summary_labels['most_common'].config(text=most_common)
            self.summary_labels['rainy_days'].config(text=f"{rainy_days} days")
            
        except Exception as e:
            print(f"Error loading 30-day summary: {e}")
            self.clear_30_day_summary()

    def load_this_day_last_year(self):
        """Load and display weather from this day last year"""
        try:
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            last_year_date = today.replace(year=today.year - 1)
            
            start_date = last_year_date - timedelta(days=2)
            end_date = last_year_date + timedelta(days=2)
            
            data = Daily(self.location_coords, start_date, end_date)
            df = data.fetch()
            
            if not df.empty:
                row = df.loc[last_year_date] if last_year_date in df.index else df.iloc[len(df) // 2]
                
                temp_c = row['tavg'] if not pd.isna(row['tavg']) else row['tmax']
                temp_f = (temp_c * 9/5) + 32 if not pd.isna(temp_c) else None

                day_data = {
                    'tavg': row['tavg'] if not pd.isna(row['tavg']) else None,
                    'tmax': row['tmax'] if not pd.isna(row['tmax']) else None,
                    'prcp': row['prcp'] if not pd.isna(row['prcp']) else 0,
                    'snow': row['snow'] if not pd.isna(row['snow']) else 0
                }
                description = self.get_weather_description_simple(day_data)
                
                self.last_year_date_label.config(text=last_year_date.strftime("%B %d, %Y"))
                self.last_year_temp_label.config(text=f"{temp_f:.0f}°F" if temp_f else "--°F")
                self.last_year_desc_label.config(text=description)
                self.update_temperature_comparison(temp_f)
            else:
                self.clear_last_year_section()
                
        except Exception as e:
            print(f"Error loading last year data: {e}")
            self.clear_last_year_section()
    
    def update_temperature_comparison(self, last_year_temp_f):
        """Update the temperature comparison with current weather"""
        try:
            if last_year_temp_f is None:
                self.comparison_label.config(text="vs Today: --", fg='black')
                return
                
            current_data = self.collector.fetch_weather(self.current_city)
            current_temp_f = current_data['main']['temp']
            temp_diff = current_temp_f - last_year_temp_f
            
            if abs(temp_diff) < 1:
                self.comparison_label.config(text="vs Today: Same", fg='black')
            elif temp_diff > 0:
                self.comparison_label.config(
                    text=f"vs Today: {temp_diff:.0f}°F Warmer", fg='red')
            else:
                self.comparison_label.config(
                    text=f"vs Today: {abs(temp_diff):.0f}°F Cooler", fg='blue')
                
        except Exception as e:
            print(f"Error comparing temperatures: {e}")
            self.comparison_label.config(text="vs Today: --", fg='black')
    
    def is_nan(self, value):
        """Robust check for NaN, pd.NA, or None"""
        try:
            return pd.isna(value)
        except:
            return True
    
    def get_weather_description_simple(self, day_data):
        """Determine weather description from data"""
        if day_data['prcp'] > 2:
            return "Rainy"
        elif day_data['snow'] > 0:
            return "Snowy"
        else:
            temp = day_data['tavg'] if day_data['tavg'] is not None else day_data['tmax']
            if temp is not None:
                temp_f = (temp * 9/5) + 32
                if temp_f > 77:
                    return "Sunny"
                elif temp_f < 50:
                    return "Cloudy"
                else:
                    return "Partly Cloudy"
            else:
                return "Clear"
    
    def clear_7_day_table(self):
        """Clear the 7-day table on error"""
        print("Clearing 7-day table")
        for i, row_data in enumerate(self.last_7_rows):
            for j, cell in enumerate(row_data):
                cell.config(text="--")
                print(f"Cleared cell [{i}][{j}]")
    
    def clear_30_day_summary(self):
        """Clear 30-day summary on error"""
        for label in self.summary_labels.values():
            label.config(text="--")
    
    def clear_last_year_section(self):
        """Clear last year section on error"""
        today = datetime.now()
        today_date = today.date()
        last_year_date = today_date.replace(year=today_date.year - 1)
        self.last_year_date_label.config(text=last_year_date.strftime("%B %d, %Y"))
        self.last_year_temp_label.config(text="--°F")
        self.last_year_desc_label.config(text="No data available")
        self.comparison_label.config(text="vs Today: --", fg='black')
    
    def show_error(self, error_message):
        """Display error message"""
        self.clear_7_day_table()
        self.clear_30_day_summary()
        self.clear_last_year_section()
        print(f"Weather Rewind Error: {error_message}")