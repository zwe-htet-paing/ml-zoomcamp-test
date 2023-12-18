import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib
import re
import string
import nltk
from nltk.corpus import stopwords

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

def load_and_preprocess_data():
    # Load data
    data_true = pd.read_csv('dataset/True.csv')
    data_fake = pd.read_csv('dataset/Fake.csv')

    # Assign class to dataset
    data_fake['class'] = 0
    data_true['class'] = 1

    data_merge = pd.concat([data_fake, data_true], axis=0)

    # Clean and preprocess text
    data_merge['text'] = data_merge['text'].apply(clean_text)

    # Shuffling
    data_merge = data_merge.sample(frac=1)
    data_merge.reset_index(inplace=True, drop=True)

    return data_merge

def train_decision_tree_model(x_train, y_train):
    # Vectorization
    vectorization = TfidfVectorizer()
    xv_train = vectorization.fit_transform(x_train)

    # Train Decision Tree model
    dt = DecisionTreeClassifier(random_state=1)
    dt.fit(xv_train, y_train)

    return dt, vectorization

def evaluate_model(model, vectorizer, x_train, y_train, x_test, y_test):
    # Vectorize test data
    xv_train = vectorizer.transform(x_train)
    xv_test = vectorizer.transform(x_test)

    # Evaluate the model
    train_accuracy = accuracy_score(y_train, model.predict(xv_train))
    test_accuracy = accuracy_score(y_test, model.predict(xv_test))

    print(f"Train Accuracy: {train_accuracy}")
    print(f"Test Accuracy: {test_accuracy}")

def save_model_and_vectorizer(model, vectorizer):
    # Save the model and vectorizer
    joblib.dump(vectorizer, 'vectorizer.pkl')
    joblib.dump(model, 'dt_model.pkl')

def main():
    # Load and preprocess data
    data = load_and_preprocess_data()

    # Split data into train and test sets
    x_train, x_test, y_train, y_test = train_test_split(data['text'], data['class'], test_size=0.25)

    # Train Decision Tree model
    dt_model, vectorization = train_decision_tree_model(x_train, y_train)

    # Evaluate the model
    evaluate_model(dt_model, vectorization, x_train, y_train, x_test, y_test)

    # Save the model and vectorizer
    save_model_and_vectorizer(dt_model, vectorization)

if __name__ == "__main__":
    main()
