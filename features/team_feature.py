import csv
import random
import os
import tkinter as tk
from datetime import datetime


class QuoteManager:
    """Manages loading and displaying inspirational quotes from CSV files"""
    
    def __init__(self, quotes_directory="team_quotes_combined"):
        self.quotes_directory = quotes_directory
        self.quotes = []
        self.load_all_quotes()
        
    def load_all_quotes(self):
        """Load quotes from all CSV files in the quotes directory"""
        self.quotes = []
        
        # Check if directory exists
        if not os.path.exists(self.quotes_directory):
            print(f"Quotes directory '{self.quotes_directory}' not found")
            return
            
        # Get all CSV files in the directory
        csv_files = [f for f in os.listdir(self.quotes_directory) if f.endswith('.csv')]
        
        for csv_file in csv_files:
            file_path = os.path.join(self.quotes_directory, csv_file)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    # Try different CSV reading approaches
                    content = file.read().strip()
                    if not content:
                        continue
                        
                    # Reset file pointer
                    file.seek(0)
                    
                    # Try to detect if it has headers
                    csv_reader = csv.reader(file)
                    rows = list(csv_reader)
                    
                    for row in rows:
                        if row:  # Skip empty rows
                            # Take the first non-empty cell as the quote
                            quote = next((cell.strip() for cell in row if cell.strip()), None)
                            if quote and len(quote) > 10:  # Basic validation
                                self.quotes.append({
                                    'text': quote,
                                    'source': csv_file.replace('.csv', '').replace('_', ' ').title()
                                })
                                
            except Exception as e:
                print(f"Error reading {csv_file}: {e}")
                continue
        
        print(f"Loaded {len(self.quotes)} quotes from {len(csv_files)} files")
        
        # Add backup quotes if no quotes were loaded
        if not self.quotes:
            self.quotes = [
                {'text': "Every day is a new beginning.", 'source': 'Default'},
                {'text': "The weather may change, but your spirit remains constant.", 'source': 'Default'},
                {'text': "Sunshine is the best medicine.", 'source': 'Default'}
            ]
    
    def get_daily_quote(self):
        """Get a quote for today (same quote all day)"""
        if not self.quotes:
            return "Stay positive and have a great day!"
            
        # Use today's date as seed for consistent daily quote
        today = datetime.now().strftime('%Y-%m-%d')
        random.seed(today)
        quote_data = random.choice(self.quotes)
        
        # Reset random seed
        random.seed()
        
        return quote_data['text']
    
    def get_random_quote(self):
        """Get a completely random quote"""
        if not self.quotes:
            return "Stay positive and have a great day!"
        
        quote_data = random.choice(self.quotes)
        return quote_data['text']


class ScrollingQuote:
    """Creates a scrolling marquee effect for quotes"""
    
    def __init__(self, parent_widget, quote_manager, width=600):
        self.parent = parent_widget
        self.quote_manager = quote_manager
        self.width = width
        
        # Create container for the scrolling area
        self.quote_container = tk.Frame(
            parent_widget,
            bg='#FFF8DC',
            relief='ridge',
            bd=1,
            height=35
        )
        self.quote_container.pack_propagate(False)
        
        # Create the scrolling label
        self.quote_label = tk.Label(
            self.quote_container,
            text="",
            font=('Arial', 10, 'italic'),
            bg='#FFF8DC',
            fg='#333333',
            anchor='w'
        )
        
        # Animation variables
        self.current_quote = ""
        self.scroll_position = 0
        self.animation_job = None
        self.scroll_speed = 50  # milliseconds between updates
        self.scroll_step = 2    # pixels to move each update
        
        # Initialize with today's quote
        self.update_quote()
    
    def pack(self, **kwargs):
        """Allow the quote widget to be packed"""
        self.quote_container.pack(**kwargs)
    
    def update_quote(self):
        """Update to today's quote"""
        self.current_quote = f"💭 Daily Inspiration: {self.quote_manager.get_daily_quote()}"
        self.reset_scroll()
    
    def reset_scroll(self):
        """Reset scrolling animation to beginning"""
        self.scroll_position = self.width
        self.start_scrolling()
    
    def start_scrolling(self):
        """Start the scrolling animation"""
        if self.animation_job:
            self.quote_container.after_cancel(self.animation_job)
        
        self._animate_scroll()
    
    def stop_scrolling(self):
        """Stop the scrolling animation"""
        if self.animation_job:
            self.quote_container.after_cancel(self.animation_job)
            self.animation_job = None
    
    def _animate_scroll(self):
        """Handle the scrolling animation"""
        if not self.current_quote:
            return
        
        # Update the label position and text
        self.quote_label.config(text=self.current_quote)
        self.quote_label.place(x=self.scroll_position, y=7)
        
        # Move the text to the left
        self.scroll_position -= self.scroll_step
        
        # Reset position when text completely scrolls off screen
        text_width = len(self.current_quote) * 7  # Approximate character width
        if self.scroll_position < -text_width:
            self.scroll_position = self.width
        
        # Schedule next animation frame
        self.animation_job = self.quote_container.after(self.scroll_speed, self._animate_scroll)


# Simple standalone test
if __name__ == "__main__":
    # Test the quote manager
    qm = QuoteManager()
    print("Today's quote:", qm.get_daily_quote())
    print("Random quote:", qm.get_random_quote())
    print(f"Total quotes loaded: {len(qm.quotes)}")