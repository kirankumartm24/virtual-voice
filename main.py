# importing prebuilt modules
import os
import logging
import pyttsx3
logging.disable(logging.WARNING)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # disabling warnings for gpu requirements
from keras_preprocessing.sequence import pad_sequences
import numpy as np
    #from keras.models import load_model
from pickle import load
import speech_recognition as sr
import sys
#sys.path.insert(0, os.path.expanduser('~') + "/PycharmProjects/Virtual_Voice_Assistant")
sys.path.insert(0, os.path.expanduser('~')+"/Virtual-Voice-Assistant") # adding voice assistant directory to system path
# importing modules made for assistant
#from database import *
#from image_generation import generate_image
from gmail import *
from api import *
from system_operation import *
from browsing import *


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
    except KeyboardInterrupt or RuntimeError:
        return



'''# load trained model
model = load_model('..\\Data\\chat_model')

# load tokenizer object
with open('..\\Data\\tokenizer.pickle', 'rb') as handle:
    tokenizer = load(handle)

# load label encoder object
with open('..\\Data\\label_encoder.pickle', 'rb') as enc:
    lbl_encoder = load(enc)'''

'''def chat(text):
    # parameters
    max_len = 20
    while True:
        result = model.predict(pad_sequences(tokenizer.texts_to_sequences([text]),truncating='post', maxlen=max_len), verbose=False)
        intent = lbl_encoder.inverse_transform([np.argmax(result)])[0]
        return intent'''

def record():
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic)
        recognizer.dynamic_energy_threshold = True
        #recognizer.energy_threshold =50000
        print("Listening...")
        audio = recognizer.listen(mic)
        try:
            text = recognizer.recognize_google(audio, language='us-in').lower()
        except:
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
                main(response)
    except KeyboardInterrupt:
        return

def main(query):
        print("ok")
        done = False
        if ("google" in query and "search" in query) or ("google" in query and "how to" in query) or "google" in query:
            googleSearch(query)
            return
        elif ("youtube" in query and "search" in query) or "play" in query or ("how to" in query and "youtube" in query) :
            youtube(query)
            return
        elif "distance" in query or "map" in query:
            get_map(query)
            return
        if  "joke" and "joke" in query:
            joke = get_joke()
            if joke:
                speak(joke)
                done = True
        elif  "news" and "news" in query:
            news = get_news()
            if news:
                speak(news)
                done = True
        elif  "ip" and "ip" in query:
            ip = get_ip()
            if ip:
                speak(ip)
                done = True
        elif  "movies" and "movies" in query:
            speak("Some of the latest popular movies are as follows :")
            get_popular_movies()
            done = True
        elif  "tv_series" and "tv series" in query:
            speak("Some of the latest popular tv series are as follows :")
            get_popular_tvseries()
            done = True
        elif "weather" and "weather" in query:
            city = re.search(r"(in|of|for) ([a-zA-Z]*)", query)
            if city:
                city = city.group(2).strip()
                weather = get_weather(city)
                speak(weather)
            else:
                weather = get_weather()
                speak(weather)
            done = True
        elif "email" and "email" in query:
            speak("Type the receiver id : ")
            receiver_id = input()
            while not check_email(receiver_id):
                speak("Invalid email id\nType reciever id again : ")
                receiver_id = input()
            speak("Tell the subject of email")
            subject = record()
            speak("tell the body of email")
            body = record()
            success = send_email(receiver_id, subject, body)
            if success:
                speak('Email sent successfully')
            else:
                speak("Error occurred while sending email")
            done = True
        elif "select_text" and "select" in query:
            sys_ops.select()
            done = True
        elif "copy_text" and "copy" in query:
            sys_ops.copy()
            done = True
        elif "paste_text" and "paste" in query:
            sys_ops.paste()
            done = True
        #elif "delete_text" and "delete" in query:
        #   sys_ops.delete()
            done = True
        elif "new_file" and "new" in query:
            sys_ops.new_file()
            done = True
        elif "switch_tab" and "switch" in query and "tab" in query:
            tab_ops.switchTab()
            done = True
        elif "close_tab" and "close" in query and "tab" in query:
            tab_ops.closeTab()
            done = True
        elif "new_tab" and "new" in query and "tab" in query:
            tab_ops.newTab()
            done = True
        elif "close_window" and "close" in query:
            win_ops.closeWindow()
            done = True
        elif "switch_window" and "switch" in query:
            win_ops.switchWindow()
            done = True
        elif "minimize_window" and "minimize" in query:
            win_ops.minimizeWindow()
            done = True
        elif "maximize_window" and "maximize" in query:
            win_ops.maximizeWindow()
            done = True
        elif "screenshot" and "screenshot" in query:
            win_ops.Screen_Shot()
            done = True
        elif "stopwatch":
            pass
        elif "wikipedia" and ("tell" in query or "about" in query):
            description = tell_me_about(query)
            if description:
                speak(description)
            else:
                googleSearch(query)
            done = True
        elif "math":
            answer = get_general_response(query)
            if answer:
                speak(answer)
                done = True
        elif "open_website":
            completed = open_specified_website(query)
            if completed:
                done = True
        elif "open_app":
            completed = open_app(query)
            if completed:
                done = True
        elif "note" and "note" in query:
            speak("what would you like to take down?")
            note = record()
            take_note(note)
            done = True
        elif "exit" and ("exit" in query or "terminate" in query or "quit" in query):
            exit(0)
        if not done:
            answer = get_general_response(query)
            if answer:
                speak(answer)
            else:
                speak("Sorry, not able to answer your query")
        return


if __name__ == "__main__":
    try:
        listen_audio()
    except:
        print("EXITED")