import datetime
import re
import requests
from newsapi import NewsApiClient
import requests
import re
import webbrowser
import re
import wikipedia
import websites

# Replace the API keys here directly or use environment variables
NEWS = 'e6d882611c8b46c0abe512bacd551144' 
API_KEY = '37b8d347a274e6b7599dfdb037c12d3b'
TMDB = '6915eaaf46eb5b98163c14caad6caf06'  

news = NewsApiClient(api_key=NEWS)


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
    categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    final_output = []

    for category in categories:
        try:
            important_news = []
            top_headlines = news.get_top_headlines(country="us", category=category)
            articles = top_headlines.get('articles', [])
            if not articles:
                continue  
            for article in articles:
                title = article['title']
                clean_title = re.sub(r'[|-] [A-Za-z0-9 |:.]*', '', title).replace("’", "'")
                if "breaking" in clean_title.lower() or "urgent" in clean_title.lower():
                    important_news.append(clean_title)
            if important_news:
                final_output.extend(important_news[:2])
            else:
                final_output.append(articles[0]['title'])  

        except requests.exceptions.RequestException:
            continue  

    # If no news was gathered, fetch a fallback from the "general" category
    if not final_output:
        fallback_headlines = news.get_top_headlines(country="us", category="general").get('articles', [])
        if fallback_headlines:
            final_output.append(fallback_headlines[0]['title'])

    return final_output  


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
        data = response # Store parsed JSON separately
        movies = data["results"]
        return [movie["title"] for movie in movies]
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
        tv_series = response["results"]
        return [show["name"] for show in tv_series]
    except KeyError:
        return None


def googleSearch(query):
	if 'image' in query:
		query += "&tbm=isch"
	#query = re.sub(r'\b(images|image|search|show|google|tell me about|for)\b', '', query)

	query = query.replace('images', '')
	query = query.replace('image', '')
	query = query.replace('search', '')
	query = query.replace('show', '')
	query = query.replace('google', '')
	query = query.replace('tell me about', '')
	query = query.replace('for', '')
	query = query.replace('open','')

	webbrowser.open("https://www.google.com/search?q=" + query)
	return "Here you go..."

def youtube(query):
	#query = re.sub(r'\b(on youtube|play|youtube)\b', '', query)

	query = query.replace('play',' ')
	query = query.replace('on youtube', ' ')
	query = query.replace('youtube', ' ')
	query = query.replace('open',' ')

	print("Searching for videos...")
	print("Finished searching!")
	video_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
	webbrowser.open(video_url)
	return "Enjoy..."

def open_specified_website(query):
	match = re.search(r"(open|go to|visit)?\s*([\w.-]+)", query, re.IGNORECASE)
	if match:
		website = match.group(2).lower()  # Extract the website name
		if website in websites.websites_dict:  # Access the imported dictionary
			url = websites.websites_dict[website]
			webbrowser.open(url)
			print(f"Opening {website}...")
			return True
		else:
			print(f"Sorry, I don't have {website} in my database.")
			return False
	else:
		print("Invalid query format.")
		return False

def tell_me_about(query):
	try:
		topic = query.replace("tell me about ", "") #re.search(r'([A-Za-z]* [A-Za-z]* [A-Za-z]*)$', query)[1]
		result = wikipedia.summary(topic, sentences=3)
		result = re.sub(r'\[.*]', '', result)
		return result
	except (wikipedia.WikipediaException, Exception) as e:
		return None

def get_map(query):
	webbrowser.open(f'https://www.google.com/maps/search/{query}')