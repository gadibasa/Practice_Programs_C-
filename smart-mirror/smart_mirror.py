from __future__ import print_function
import requests
from tkinter import *
import datetime
import pickle
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import threading

# Weather API Configuration
WEATHER_API_KEY = '32931711086ca7d195caf075deba7ccb'  # OpenWeatherMap API key
CITY = 'Pune'
WEATHER_URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}'

# Google Calendar API Configuration
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# News API Configuration
NEWS_API_KEY = '5da633d4284d4b66b23b47962d4eb00a'  # NewsAPI key
NEWS_URL = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}'

def get_weather():
    print("Fetching weather...")
    response = requests.get(WEATHER_URL, timeout=10)
    data = response.json()
    if 'weather' in data:
        main = data['weather'][0]['main']
        temperature = data['main']['temp']
        temp_celsius = temperature - 273.15
        print(f"Weather fetched: {main}, {temp_celsius:.2f}°C")
        return main, temp_celsius
    else:
        print("Weather data not available")
        return "N/A", "N/A"

def get_calendar_events():
    print("Fetching calendar events...")
    events = []
    try:
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        print(f"Calendar events fetched: {len(events)}")
    except Exception as e:
        print(f"Error fetching calendar events: {e}")
    return events

def get_news():
    print("Fetching news...")
    try:
        response = requests.get(NEWS_URL, timeout=10)
        data = response.json()
        print(f"NewsAPI response: {data}")  # Detailed logging of the API response
        if 'articles' in data:
            headlines = [article['title'] for article in data['articles']]
            print(f"News fetched: {len(headlines)} articles")
            return headlines
        else:
            print("News data not available")
            return ["No news available"]
    except Exception as e:
        print(f"Error fetching news: {e}")
        return ["Error fetching news"]

def update_display():
    print("Updating display...")
    main, temp_celsius = get_weather()
    weather_label.config(text=f'Weather: {main}')
    if temp_celsius != "N/A":
        temp_label.config(text=f'Temperature: {temp_celsius:.2f}°C')
    else:
        temp_label.config(text='Temperature: N/A')

    events = []
    def fetch_calendar_events():
        nonlocal events
        try:
            events = get_calendar_events()
        except Exception as e:
            print(f"Error during calendar fetch: {e}")

    calendar_thread = threading.Thread(target=fetch_calendar_events)
    calendar_thread.start()
    calendar_thread.join(timeout=20)  # Timeout after 20 seconds

    if calendar_thread.is_alive():
        print("Calendar request timed out.")
        events_label.config(text='No upcoming events found or request timed out.')
    else:
        events_text = ""
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            events_text += f"{start}: {event['summary']}\n"
        events_label.config(text=events_text)

    headlines = get_news()
    news_label.config(text='\n'.join(headlines[:5]))  # Display the top 5 headlines

    print("Display updated.")
    root.after(60000, update_display)

root = Tk()
root.title('Smart Mirror - All Features')

weather_label = Label(root, font=('Helvetica', 20))
weather_label.pack(pady=10)

temp_label = Label(root, font=('Helvetica', 20))
temp_label.pack(pady=10)

events_label = Label(root, font=('Helvetica', 15), justify=LEFT, wraplength=400)
events_label.pack(pady=10)

news_label = Label(root, font=('Helvetica', 15), justify=LEFT, wraplength=400)
news_label.pack(pady=10)

print("Starting application...")
update_display()
print("Application running.")
root.mainloop()
