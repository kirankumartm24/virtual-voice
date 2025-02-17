import webbrowser
import re
import wikipedia
import websites


def googleSearch(query):
	if 'image' in query:
		query += "&tbm=isch"
	query = query.replace('images', '')
	query = query.replace('image', '')
	query = query.replace('search', '')
	query = query.replace('show', '')
	query = query.replace('google', '')
	query = query.replace('tell me about', '')
	query = query.replace('for', '')
	webbrowser.open("https://www.google.com/search?q=" + query)
	return "Here you go..."

def youtube(query):
	query = query.replace('play', ' ')
	query = query.replace('on youtube', ' ')
	query = query.replace('youtube', ' ')

	print("Searching for videos...")
	print("Finished searching!")
	video_url=(f'https://www.youtube.com/results?search_query={query.replace('','+')}')
	webbrowser.open(video_url)
	return "Enjoy..."

def open_specified_website(query):
	website = query[5:] #re.search(r'[a-zA-Z]* (.*)', query)[1]
	if website in websites.websites_dict:
		url = websites.websites_dict[website]
		webbrowser.open(url)
		return True
	else:
		return None

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