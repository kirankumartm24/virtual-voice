import os
import datetime
import re
import requests
from wolframalpha import Client

# Replace the API keys here directly or use environment variables
NEWS = 'your_news_api_key'  # Replace with your NewsAPI key
WOLFRAMALPHA = 'your_wolframalpha_api_key'  # Replace with your WolframAlpha API key
API_KEY = '37b8d347a274e6b7599dfdb037c12d3b'
TMDB = 'your_tmdb_api_key'  # Replace with your TMDB API key

#news = NewsApiClient(api_key=NEWS)

def get_ip(_return=False):
    try:
        response = requests.get(f'http://ip-api.com/json/').json()
        if _return:
            return response
        else:
            return f'Your IP address is {response["query"]}'
    except KeyboardInterrupt:
        return None
    except requests.exceptions.RequestException:
        return None

def get_joke():
    try:
        joke = requests.get('https://v2.jokeapi.dev/joke/Any?format=txt').text
        return joke
    except KeyboardInterrupt:
        return None
    except requests.exceptions.RequestException:
        return None

def get_news():
    try:
        top_news = ""
        top_headlines = news.get_top_headlines(language="en", country="in")
        for i in range(10):
             top_news += re.sub(r'[|-] [A-Za-z0-9 |:.]*', '', top_headlines['articles'][i]['title']).replace("’", "'") + '\n'
        return top_news
    except KeyboardInterrupt:
        return None
    except requests.exceptions.RequestException:
        return None

def get_weather(city=''):
    if not city:
        city = 'Nandyal'  # You can replace this with your city or logic to detect location
    
    # Make API call to OpenWeather
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric').json()
    print(f"API Response: {response}")
    
    if response.get('cod') != 200:
        return "Sorry, I couldn't fetch the weather information."

    # Format weather response
    weather = f'It\'s {response["main"]["temp"]}° Celsius and {response["weather"][0]["main"]}. ' \
               f'It feels like {response["main"]["feels_like"]}° Celsius.\n' \
               f'Wind speed: {round(response["wind"]["speed"] * 3.6, 2)} km/h.\n' \
               f'Visibility: {int(response["visibility"] / 1000)} km.'
    return weather

def get_general_response(query):
    client = Client(app_id=WOLFRAMALPHA)
    try:
        response = client.query(query)
        return next(response.results).text
    except (StopIteration, AttributeError) as e:
        return None
    except KeyboardInterrupt:
        return None

def get_popular_movies():
    try:
        response = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB}&region=IN&sort_by=popularity.desc&"f"primary_release_year={datetime.date.today().year}").json()
    except requests.exceptions.RequestException:
        return None
    try:
        print()
        for movie in response["results"]:
            title = movie['title']
            print(title)
    except KeyError:
        return None

def get_popular_tvseries():
    try:
        response = requests.get(f"https://api.themoviedb.org/3/tv/popular?api_key={TMDB}&region=IN&sort_by=popularity.desc&"
                                f"primary_release_year={datetime.date.today().year}").json()
    except requests.exceptions.RequestException:
        return None
    try:
        print()
        for show in response["results"]:
            title = show['name']
            print(title)
    except KeyError:
        return None
