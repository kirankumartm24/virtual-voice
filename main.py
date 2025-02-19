import os
import logging
import pyttsx3
import speech_recognition as sr
import re
from gmail import *
from api import *
from system_operation import *
from browsing import *
from nltk.tokenize import word_tokenize
import webbrowser
import datetime

logging.disable(logging.WARNING)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

recognizer = sr.Recognizer()

engine = pyttsx3.init()
engine.setProperty('rate', 185)

sys_ops = SystemTasks()
tab_ops = TabOpt()
win_ops = WindowOpt()

def speak(text):
    print("ASSISTANT -> " + text)
    try:
        engine.say(text)
        engine.runAndWait()
    except (KeyboardInterrupt, RuntimeError):
        return

def record():
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic)
        recognizer.dynamic_energy_threshold = True
        #recognizer.energy_threshold =50000
        print("Listening...")
        audio = recognizer.listen(mic)
        try:
            text = recognizer.recognize_google(audio, language='en-US').lower()
        except :
            return None
    print("USER -> " + text)
    return text


def listen_audio():
    try:
        while True:
            response = record()
            if response is None:
                continue
            else:
                sentences = word_tokenize(response)
                ses= " ".join(sentences)
                main(ses)
    except KeyboardInterrupt:
        return


def main(query):
    done = False

    # Simple greetings
    if "hello" in query or "hi" in query:
        speak("Hello! How can I assist you today?")
        done = True

    # Search related queries
    elif "google" in query and "search" in query:
        googleSearch(query)
        speak("Here are the results I found on Google.")
        done = True
    elif "youtube" in query and "search" in query or "play" in query or ("open" in query and "youtube" in query):
        youtube(query)
        speak("Here are the results from YouTube.")
        done = True
    elif "map" in query or "distance" in query:
        get_map(query)
        speak("Here are the map results.")
        done = True
    elif "open instagram" in query:
        speak("Opening Instagram...")
        webbrowser.open("https://instagram.com/")
    # Jokes and news
    elif "joke" in query:
        joke = get_joke()
        if joke:
            speak(joke)
            done = True
    elif "news" in query:
        news = get_new()
        if news:
            speak(news)
            done = True
    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")
    elif "date" in query:
        current_date = datetime.datetime.now().strftime("%d %B, %Y")
        speak(f"Today's date is {current_date}")

    # System operations
    elif "ip" in query or "current location" in query:
        ip = get_ip()
        if ip:
            speak(f"Your current IP address is {ip}.")
            done = True
    elif "weather" in query:
        city = re.search(r"(in|of|for) ([a-zA-Z]*)", query)
        if city:
            city = city.group(2).strip()
            weather = get_weather(city)
            speak(f"The weather in {city} is: {weather}")
        else:
            weather = get_weather()
            speak(f"The weather is: {weather}")
        done = True

    # Email functionality
    elif "email" in query:
        speak("Please say the recipient's email address.")
        receiver_id = record()
        while not check_email(receiver_id):
            speak("Invalid email address. Please say it again.")
            receiver_id = record()
        
        speak("Say the subject of the email.")
        subject = record()
        
        speak("Say the body of the email.")
        body = record()
        
        success = send_email(receiver_id, subject, body)
        if success:
            speak("Your email has been sent successfully.")
        else:
            speak("There was an error sending the email.")
        done = True

    # Other system tasks
    elif "select text" in query:
        sys_ops.select()
        speak("The text has been selected.")
        done = True
    elif "copy text" in query:
        sys_ops.copy()
        speak("The text has been copied.")
        done = True
    elif "paste text" in query:
        sys_ops.paste()
        speak("The text has been pasted.")
        done = True
    elif "open website" in query:
        completed = open_specified_website(query)
        if completed:
            speak("Opening the website.")
            done = True
    elif "open app" in query:
        completed = open_app(query)
        if completed:
            speak("Opening the app.")
            done = True
    elif "exit" in query or "terminate" in query or "quit" in query:
        speak("thank you!")
        exit(0)
    if not done:
                answer =tell_me_about(query)
                if answer:
                    speak(answer)
                else:
                    speak("Sorry, not able to answer your query")
    return


if __name__ == "__main__":
    listen_audio()

