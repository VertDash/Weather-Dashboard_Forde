import tkinter as tk

root=tk.Tk()    
root.title("Weather App")
root.geometry("600x400")

label = tk.Label(root,text="Welcome to the Weather App")
label.pack(pady=20)

root.mainloop()
