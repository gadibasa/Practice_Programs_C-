import requests
from tkinter import *

# Replace 'your_api_key' with your NewsAPI key
API_KEY = '5da633d4284d4b66b23b47962d4eb00a'  # Make sure to replace this with your actual API key
NEWS_URL = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={API_KEY}'

def get_news():
    response = requests.get(NEWS_URL)
    data = response.json()
    print(data)  # Print the API response for debugging
    if 'articles' in data:
        headlines = [article['title'] for article in data['articles']]
        return headlines
    else:
        print("Error: 'articles' key not found in the response")
        return ["No news available"]

def update_news():
    headlines = get_news()
    news_label.config(text='\n'.join(headlines[:5]))  # Display the top 5 headlines
    root.after(60000, update_news)

root = Tk()
root.title('Smart Mirror - News Feed')

news_label = Label(root, font=('Helvetica', 15), justify=LEFT, wraplength=400)
news_label.pack(pady=20)

update_news()
root.mainloop()
