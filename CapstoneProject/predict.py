import pandas as pd
import joblib  # Use joblib for model loading

import re
import string
import nltk
from nltk.corpus import stopwords

from flask import Flask, request, jsonify

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    """
    Clean and preprocess text data.

    Parameters:
    - text (str): Input text to be cleaned.

    Returns:
    - str: Cleaned text.
    """
    # Convert to lowercase
    text = text.lower()

    # Remove square brackets and content inside them
    text = re.sub(r'\[.*?\]', '', text)

    # Replace non-word characters with space
    text = re.sub(r'\W', ' ', text)

    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    # Remove HTML tags
    text = re.sub(r'<.*?>+', '', text)

    # Remove punctuation
    text = re.sub(r'[{}]'.format(re.escape(string.punctuation)), '', text)

    # Remove newline characters
    text = re.sub(r'\n', '', text)

    # Remove words containing digits
    text = re.sub(r'\w*\d\w*', '', text)

    # Remove stopwords
    text = ' '.join(word for word in text.split() if word not in stop_words)

    return text

def output_label(n):
    """
    Convert numerical label to human-readable label.

    Parameters:
    - n (int): Numerical label (0 or 1).

    Returns:
    - str: Human-readable label.
    """
    return "Fake News" if n == 0 else "Not A Fake News"


vectorizer = joblib.load('vectorizer.pkl')
model = joblib.load('dt_model.pkl')

app = Flask('Fake News Detection')

@app.route('/predict', methods=['POST'])
def predict():
    client = request.get_json()
  
    # Clean the text
    cleaned_news = clean_text(client)

    # Vectorize the cleaned text
    news_vectorized = vectorizer.transform([cleaned_news])

    # Predict using the loaded DT model
    y_pred = model.predict(news_vectorized)

    label = output_label(y_pred[0])

    result = {
        'probability': float(y_pred),
        'label': label
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=9696)
    # app.run(debug=True, host='0.0.0.0', port=9696)