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
                    
                    # Extract author name from filename (remove .csv and clean up)
                    author_name = self._extract_author_name(csv_file)
                    
                    for row in rows:
                        if row:  # Skip empty rows
                            # Check if this is a header row (skip common header terms)
                            first_cell = row[0].strip().lower()
                            if first_cell in ['quote', 'quotes', 'text', 'saying', 'inspiration']:
                                continue
                                
                            # Handle different CSV formats
                            quote_text = None
                            quote_author = "Unknown"  # Default to Unknown
                            
                            if len(row) >= 2:
                                # Two columns: assume quote, author
                                quote_text = row[0].strip()
                                if row[1].strip():  # If author column has content, use it
                                    quote_author = row[1].strip()
                            else:
                                # Single column: just the quote, author stays "Unknown"
                                quote_text = row[0].strip()
                            
                            # Basic validation
                            if quote_text and len(quote_text) > 10:
                                self.quotes.append({
                                    'text': quote_text,
                                    'author': quote_author,
                                    'source': csv_file.replace('.csv', '').replace('_', ' ').title()
                                })
                                
            except Exception as e:
                print(f"Error reading {csv_file}: {e}")
                continue
        
        print(f"Loaded {len(self.quotes)} quotes from {len(csv_files)} files")
        
        # Add fallback quotes if no quotes were loaded
        if not self.quotes:
            self.quotes = [
                {'text': "Every day is a new beginning.", 'author': 'Unknown', 'source': 'Default'},
                {'text': "The weather may change, but your spirit remains constant.", 'author': 'Weather Wisdom', 'source': 'Default'},
                {'text': "Sunshine is the best medicine.", 'author': 'Nature', 'source': 'Default'}
            ]
    
    def _extract_author_name(self, filename):
        """Extract a clean author name from the CSV filename"""
        # Remove .csv extension
        name = filename.replace('.csv', '')
        
        # Handle different naming patterns
        if '_' in name:
            # Handle patterns like "Juice_Kemp" or "Tiffani_Quotes1"
            parts = name.split('_')
            if len(parts) >= 2:
                # If last part looks like "Quotes" or similar, ignore it
                if parts[-1].lower().startswith('quote'):
                    name_parts = parts[:-1]
                else:
                    name_parts = parts
                
                # Capitalize each part
                clean_name = ' '.join(word.capitalize() for word in name_parts)
            else:
                clean_name = name.capitalize()
        else:
            # Single word filename
            if name.lower() == 'quotes':
                clean_name = 'Anonymous'
            else:
                clean_name = name.capitalize()
        
        return clean_name
    
    def get_daily_quote(self):
        """Get a quote for today (same quote all day) with author"""
        if not self.quotes:
            return "Stay positive and have a great day! — Unknown"
            
        # Use today's date as seed for consistent daily quote
        today = datetime.now().strftime('%Y-%m-%d')
        random.seed(today)
        quote_data = random.choice(self.quotes)
        
        # Reset random seed
        random.seed()
        
        return f"{quote_data['text']} — {quote_data['author']}"
    
    def get_random_quote(self):
        """Get a completely random quote with author"""
        if not self.quotes:
            return "Stay positive and have a great day! — Unknown"
        
        quote_data = random.choice(self.quotes)
        return f"{quote_data['text']} — {quote_data['author']}"
    
    def get_daily_quote_data(self):
        """Get full quote data for today (for advanced formatting)"""
        if not self.quotes:
            return {'text': "Stay positive and have a great day!", 'author': 'Unknown', 'source': 'Default'}
            
        # Use today's date as seed for consistent daily quote
        today = datetime.now().strftime('%Y-%m-%d')
        random.seed(today)
        quote_data = random.choice(self.quotes)
        
        # Reset random seed
        random.seed()
        
        return quote_data


class ScrollingQuote:
    """Creates a scrolling marquee effect for quotes with author attribution"""
    
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
        """Update to today's quote with author"""
        quote_with_author = self.quote_manager.get_daily_quote()
        self.current_quote = f"💭 Daily Inspiration: {quote_with_author}"
        self.reset_scroll()
    
    def update_quote_advanced(self):
        """Update with advanced formatting (optional method for future use)"""
        quote_data = self.quote_manager.get_daily_quote_data()
        formatted_quote = f"💭 \"{quote_data['text']}\" — {quote_data['author']}"
        self.current_quote = formatted_quote
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
    
    # Show some example quotes with authors
    if qm.quotes:
        print("\nSample quotes:")
        for i, quote in enumerate(qm.quotes[:3]):
            print(f"{i+1}. \"{quote['text']}\" — {quote['author']}")