import requests
from tkinter import *

# Replace 'your_api_key' with your OpenWeatherMap API key
API_KEY = '32931711086ca7d195caf075deba7ccb'  # Make sure to replace this with your actual API key
CITY = 'Pune'
WEATHER_URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}'

def get_weather():
    response = requests.get(WEATHER_URL)
    data = response.json()
    print(data)  # Print the API response for debugging
    if 'weather' in data:
        main = data['weather'][0]['main']
        temperature = data['main']['temp']
        temp_celsius = temperature - 273.15
        return main, temp_celsius
    else:
        print("Error: 'weather' key not found in the response")
        return "N/A", "N/A"

def update_weather():
    main, temp_celsius = get_weather()
    weather_label.config(text=f'Weather: {main}')
    if temp_celsius != "N/A":
        temp_label.config(text=f'Temperature: {temp_celsius:.2f}°C')
    else:
        temp_label.config(text='Temperature: N/A')
    root.after(60000, update_weather)

root = Tk()
root.title('Smart Mirror - Weather')

weather_label = Label(root, font=('Helvetica', 20))
weather_label.pack(pady=20)

temp_label = Label(root, font=('Helvetica', 20))
temp_label.pack(pady=20)

update_weather()
root.mainloop()
