import tkinter as tk

# root=tk.Tk()    
# root.title("Weather App")
# root.geometry("600x400")

# label = tk.Label(root,text="Welcome to the Weather App")
# label.pack(pady=20)

# root.mainloop()


# This is where my program begins running like the play button
from gui.main_window import WeatherApp

# This line means "only run this code if this file is run directly"
# cant be imported
# create window and wait for interaction
if __name__ == "__main__":
    app = WeatherApp() 
    app.mainloop()