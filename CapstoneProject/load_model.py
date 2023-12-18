import pandas as pd
import joblib  # Use joblib for model loading

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

# Load the Decision Tree model
dt_model_path = './dt_model.pkl'  # Replace with the actual path
dt_model = joblib.load(dt_model_path)

# Load the TfidfVectorizer used during training
vectorizer_path = './vectorizer.pkl'  # Replace with the actual path
vectorization = joblib.load(vectorizer_path)

def output_label(n):
    """
    Convert numerical label to human-readable label.

    Parameters:
    - n (int): Numerical label (0 or 1).

    Returns:
    - str: Human-readable label.
    """
    return "Fake News" if n == 0 else "Not A Fake News"

def predict_text(news):
    testing_news = {"text": [news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test["text"] = new_def_test["text"].apply(clean_text)
    new_x_test = new_def_test["text"]
    new_xv_test = vectorization.transform(new_x_test)

    pred_DT = dt_model.predict(new_xv_test)
    return output_label(pred_DT[0])

# Example usage:
news_article = "GENEVA (Reuters) - North Korea and the United States clashed at a U.N. forum on Tuesday over their military intentions towards \
    one another, with Pyongyang s envoy declaring it would  never  put its nuclear deterrent on the negotiating table. Japan, well within reach \
    of North Korea s missiles, said the world must maintain pressure on the reclusive country to rein in its nuclear and missile programs and \
    now was not the time for a resumption of multi-party talks. North Korea has pursued its weapons programs in defiance of U.N. Security \
    Council sanctions and ignored all calls, including from major ally China, to stop, prompting a bellicose exchange of rhetoric between \
    the North and the United States. North Korea justifies its weapons programs, including its recent threat to fire missiles towards \
    the U.S. Pacific territory of Guam, by pointing to perceived U.S. hostility, such as military exercises with South Korea this week.\
    U.S. disarmament ambassador Robert Wood told a U.N.-sponsored Conference on Disarmament in Geneva U.S. President Donald Trump s top priority \
    was to protect the United States and its allies against the  growing threat  from North Korea and America was ready to use  the full range of \
    capabilities  at its disposal. The  path to dialogue still remained an option  for Pyongyang and it had the choice between poverty and belligerence \
    on the one hand and prosperity and acceptance. North Korea s envoy told the same forum the North s nuclear deterrent would never be up for negotiation,\
    echoing Pyongyang s regular denunciation of U.S.  aggression .  The measures taken by the DPRK to strengthen its nuclear deterrence and \
    develop inter-continental rockets is justifiable and a legitimate option for self-defense in the face of such apparent and real threats, \
    diplomat Ju Yong Chol told the forum, referring to  constant nuclear threats  by the United States. DPRK stands for the North s official name,\
    the Democratic People s Republic of Korea. Regarding joint U.S.-South Korean military exercises that began on Monday, he warned:  \
    The ongoing military adventure would certainly add gasoline to the fire, driving the current tense situation to further deterioration. \
    Japanese Foreign Minister Taro Kono said pressure must be maintained until the North demonstrated it would give up its nuclear program. \
    It s not the time to discuss (the resumption of) six-party talks,  Kono said, referring to stalled negotiations involving both Koreas, \
    the United States, Russia, China and Japan.  It s time to exert pressure,  he told reporters. The head of the U.S. military s Pacific Command said \
    diplomacy was key. Admiral Harry Harris was in South Korea to observe annual joint military drills with the South Korean military, which the North \
    called a step towards nuclear conflict masterminded by  war maniacs .  So we hope and we work for diplomatic solutions to the challenge presented \
    by Kim Jong Un,  Harris told reporters at a U.S. air base in Osan, about an hour from Seoul, referring to the North Korean leader. \
    He said diplomacy was  the most important starting point  in response to the North s threat, when asked what actions by North Korea might trigger \
    a preemptive U.S. strike against it.  As far as a timeline, it would be crazy for me to share with you those tripwires in advance. \
    If we did that, it would hardly be a military strategy,  he said. The United States and South Korea began the long-planned exercises on Monday,\
    called the Ulchi Freedom Guardian, which the allies have said are purely defensive. The drills involve tens of thousands of troops as well as \
    computer simulations designed to prepare for war with a nuclear-capable North Korea. The United States and South Korea are technically still at war \
    with the North because their 1950-53 conflict ended in a truce, not a peace treaty.  Delegations from about 20 countries spoke at the four-hour U.N. \
    session, including Britain, France, Australia and South Korea, all of which criticized North Korea.  I would like to repeat the appeal to the DPRK \
    to listen to the fact that there is no alternative to stopping the different provocations and to return to dialogue,  South Korean ambassador \
    Kim Inchul said.  We have never threatened the DPRK with any attacks and we have never promoted the use of force."
    
prediction = predict_text(news_article)
print(f"DT Prediction: {prediction}")
