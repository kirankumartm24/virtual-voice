from flask import Flask, request, jsonify,send_file
from flask_cors import CORS
import datetime
import pickle
import re
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import logging
from gmail import send_email  # Importing the correct function
from api import *
from system_operation import *
from database import *

# Suppress TensorFlow warnings
tf.get_logger().setLevel("ERROR")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load trained intent classification model
model = tf.keras.models.load_model("intent_model.h5")

# Load tokenizer and label encoder
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)
with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Initialize system operations
sys_ops = SystemTasks()

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Requests
@app.route('/')
def home():
    return send_file('index.html')

@app.route("/predict", methods=["POST"])
def predict():
    if not request.is_json:
        return jsonify({"response": "Invalid request format."})

    data = request.json
    query = data.get("query", "").lower()
    
    if not query:
        return jsonify({"response": "I didn't catch that. Please repeat."})

    sequence = tokenizer.texts_to_sequences([query])
    if not sequence or not sequence[0]:
        return jsonify({"response": "Sorry, I am not able to answer your query."})

    padded_sequence = pad_sequences(sequence, padding="post")
    prediction = model.predict(padded_sequence)
    predicted_label = label_encoder.inverse_transform([np.argmax(prediction)])[0]

    response_text = handle_intent(predicted_label, data)
    return jsonify({"response": response_text})

def handle_intent(intent, data):
    query = data.get("query", "").lower()

    if intent == "get_time":
        return f"The time is {datetime.datetime.now().strftime('%I:%M %p')}"
    elif intent == "get_date":
        return f"Today's date is {datetime.datetime.now().strftime('%d %B, %Y')}"
    elif intent == "get_datetime":
        return f"The current date and time is {datetime.datetime.now().strftime('%A, %d %B %Y, %I:%M %p')}"
    elif intent == "greeting":
        return "Hello! How can I assist you today?"
    elif intent == "search_google":
        googleSearch(query)
        return "Here are the results I found on Google."
    elif intent == "search_youtube" or "open youtube" in query:
        youtube(query)
        return "Here are the results from YouTube."
    elif intent == "joke":
        return get_joke() or "Sorry, I couldn't find a joke right now."
    elif intent == "news":
        return get_news() or "I'm unable to fetch news at the moment."
    elif intent == "ip":
        return get_ip() or "Couldn't retrieve IP address."
    elif intent == "weather":
        return get_weather()
    elif intent == "open_website":
        return "Opening the website." if open_specified_website(query) else "Unable to open website."
    elif intent == "movies" and "movies" in query: 
        return get_popular_movies() 
    elif intent == "tv_series" and "tv series" in query: 
        return get_popular_tvseries() 
    elif intent == "select_text":
        sys_ops.select()
        return "The text has been selected."
    elif intent == "copy_text":
        sys_ops.copy()
        return "The text has been copied."
    elif intent == "paste_text":
        sys_ops.paste()
        return "The text has been pasted."
    elif intent == "get_map":
        return get_map()
    elif intent == "get_data":
        return get_data() if "history" in query else "I couldn't fetch the requested data."
    elif intent == "exit":
        return "Thank you! Goodbye."
    elif intent == "email":
        return handle_email(data)
    else:
        return tell_me_about(query)

def handle_email(data):
    receiver_email = data.get("email", "").strip()
    subject = data.get("subject", "No Subject").strip()
    body = data.get("body", "No Content").strip()

    print("Received email request:", receiver_email, subject, body)
    
    # Validate Email Format
    receiver_email = receiver_email.lower().replace(" at the rate ", "@").replace(" at ", "@").replace(" dot ", ".")
    receiver_email = receiver_email.replace(" underscore ", "_").replace(" dash ", "-")
    receiver_email = re.sub(r"\s+", "",receiver_email)
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not receiver_email or not re.match(email_regex, receiver_email):
        return "Invalid email address. Please enter a valid email."

    success = send_email(receiver_email, subject, body)
    return "Your email has been sent successfully." if success else "There was an error sending the email."

# Change this at the bottom of your app.py:
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
