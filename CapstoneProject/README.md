# Fake News Detection

DatatalksClub ML Zoomcamp Capstone Project

## Overview:

Fake news has become a significant issue in today's digital age, where information spreads rapidly through online platforms. The ability to distinguish between genuine and fake news is crucial for maintaining the integrity of information and preventing the potential harm caused by misinformation. This problem involves building a machine learning model for the detection of fake news based on textual content.

## Problem Statement:

Develop a fake news detection system that can automatically classify news articles as either genuine or fake based on the content of the text. The system should be capable of processing textual information and providing a binary classification for each news article.

## Dateset:

The dataset consists of labeled news articles, where each article is labeled as either "fake" or "real." The dataset should be appropriately preprocessed, and features such as the text content of the news articles are used for model training and evaluation. You can download the dataset [here](https://www.kaggle.com/datasets/jainpooja/fake-news-detection).


## Key Tasks:

1. Data Preprocessing:
    - Text cleaning: Remove noise, HTML tags, special characters, and irrelevant information.
    - Tokenization: Break down the text into individual words or tokens.
    - Vectorization: Convert the text data into numerical vectors, possibly using techniques like TF-IDF or word embeddings.

2. Model Selection:
    - Choose a suitable machine learning algorithm for classification. Common choices include Logistic Regression, Decision Trees, Random Forests, Gradient Boosting, or deep learning models like Recurrent Neural Networks (RNNs) or Transformers.

3. Training the Model:
    - Train the selected model on the labeled dataset, using appropriate features derived from the text content.

4. Evaluation:
    - Assess the performance of the model using evaluation metrics such as accuracy, precision, recall, F1 score, and confusion matrix.

5. Testing and Validation:
    - Manually test the model on new or unseen news articles to validate its generalization capability.

6. Fine-Tuning:
    - If necessary, fine-tune the model parameters to improve performance.


## Prerequisites:

Before you begin, ensure you have the following dependencies installed:

- Python (>=3.10)
- Pipenv
- scikit-learn
- joblib
- nltk

You can install these dependencies using the following command:

`
pipenv install
`

You can check the training process at `notebook.ipynb`

## Run Locally

- Run web server using `python predict.py`
- Open a new terminal and run  `python test_predict.py`

## Run on Docker

- `docker build -t capstone_project .`
- `docker run -it --rm -p 9696:9696 capstone_project`
- Open a new terminal and run `python test_predict.py`

## Run using docker-compose

- `docker-compose up`
- Open a new terminal and run `python test_predict.py`

