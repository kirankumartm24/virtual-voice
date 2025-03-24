import json
import numpy as np
import tensorflow as tf
import nltk
import pickle
#from nltk.tokenize import word_tokenize
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Bidirectional, Dense, Dropout, SpatialDropout1D, LayerNormalization

# Ensure required downloads
# nltk.download("punkt")

# Load JSON data
with open("data.json", "r") as file:
    data = json.load(file)

# Prepare training data
texts = []  # Input sentences
labels = []  # Corresponding intent labels

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        texts.append(pattern.lower())  # Convert to lowercase
        labels.append(intent["tag"])

# Tokenization
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)
word_index = tokenizer.word_index  # Vocabulary dictionary
vocab_size = len(word_index) + 1  # Add 1 for padding

# Convert text to sequences
sequences = tokenizer.texts_to_sequences(texts)

# Dynamic padding based on longest sentence in dataset
padded_sequences = pad_sequences(sequences, padding="post")

# Encode labels
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)
num_classes = len(set(encoded_labels))  # Unique label count
labels_categorical = tf.keras.utils.to_categorical(encoded_labels, num_classes)

# Define RNN Model (LSTM + Bidirectional LSTM for better accuracy)
embedding_dim = 100  # Word embedding dimension

model = Sequential([
    # Embedding Layer (Use Pretrained Word Embeddings if available)
    Embedding(input_dim=vocab_size, output_dim=200),  
    SpatialDropout1D(0.3),  # Prevent overfitting

    # First Bidirectional LSTM Layer
    Bidirectional(LSTM(256, return_sequences=True, dropout=0.3, recurrent_dropout=0.2)),  
    LayerNormalization(),

    # Second Bidirectional LSTM Layer (Deeper Representation)
    Bidirectional(LSTM(128, return_sequences=True, dropout=0.3, recurrent_dropout=0.2)),  
    LayerNormalization(),

    # Third LSTM Layer (Final Feature Extraction)
    LSTM(64, dropout=0.3, recurrent_dropout=0.2),  
    LayerNormalization(),

    # Fully Connected Layers
    Dense(128, activation="relu"),
    Dropout(0.5),

    Dense(num_classes, activation="softmax")  # Output Layer
])

# Compile Model
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Train Model
model.fit(padded_sequences, labels_categorical, epochs=50, batch_size=16, verbose=1, validation_split=0.1)

# Save Model and Required Files
model.save("intent_model.h5")

with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print("Training complete! Model saved.")

# Evaluate on training and validation set
train_loss, train_acc = model.evaluate(padded_sequences, labels_categorical)
print(f"Training Accuracy: {train_acc * 100:.2f}%")

# If you have a separate test dataset, use:
