import os
import requests
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def get_weather_data(location, api_key):
    """Fetches weather data for a given location using the OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("Error", f"Failed to fetch data. Error code: {response.status_code}")

def display_weather_data(data):
    """Displays weather data in a user-friendly format."""
    temp_kelvin = data['main']['temp']
    temp_celsius = round(temp_kelvin - 273.15, 2)
    humidity = data['main']['humidity']
    conditions = data['weather'][0]['description']
    weather_icon = data['weather'][0]['icon']
    icon_url = f"http://openweathermap.org/img/wn/{weather_icon}.png"

    weather_label.config(text=f"Temperature: {temp_celsius}°C\nHumidity: {humidity}%\nConditions: {conditions}")
    
    # Load weather icon based on weather condition
    icon_path = f"icons/{weather_icon}.png"
    if not os.path.exists("icons"):
        os.makedirs("icons")
    try:
        response = requests.get(icon_url)
        if response.status_code == 200:
            with open(icon_path, "wb") as f:
                f.write(response.content)
            img = Image.open(icon_path)
            photo = ImageTk.PhotoImage(img)
            weather_icon_label.config(image=photo)
            weather_icon_label.image = photo
        else:
            messagebox.showerror("Error", "Failed to fetch weather icon.")
    except Exception as e:
        print("Error:", e)

def search_weather():
    location = location_entry.get()
    api_key = "d0fac1468274bbcea8188b4776bfc21e"
    if location:
        data = get_weather_data(location, api_key)
        if data:
            display_weather_data(data)
    else:
        messagebox.showerror("Error", "Please enter a location.")

root = tk.Tk()
root.title("Weather App")
root.geometry("300x400")
root.configure(bg="#f0f0f0")

# Load background image
bg_image_path = "back.jpg"
if os.path.exists(bg_image_path):
    img = Image.open(bg_image_path)
    img_width, img_height = img.size
    window_width, window_height = 300, 400  # Initial window size
    scale = max(window_width / img_width, window_height / img_height)
    img = img.resize((int(img_width * scale), int(img_height * scale)), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(img)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo
else:
    messagebox.showerror("Error", "Background image not found.")

style = ttk.Style()
style.configure('My.TFrame', background='#ffffff')

frame = ttk.Frame(root, padding=10, style='My.TFrame')
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
frame.config(borderwidth=2, relief="groove")

location_label = ttk.Label(frame, text="Enter a city name or ZIP code:")
location_label.grid(row=0, column=0, padx=(0, 10), pady=(10, 0), sticky=tk.W)

location_entry = ttk.Entry(frame, width=20)
location_entry.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky=tk.E)

search_button = ttk.Button(frame, text="Search", command=search_weather)
search_button.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky=tk.EW)

weather_label = ttk.Label(frame, text="")
weather_label.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)

weather_icon_label = ttk.Label(frame)
weather_icon_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))

root.mainloop()
