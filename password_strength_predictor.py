import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

def load_xgboost_model(model_path):
    # Load the XGBoost model from the given model_path
    return joblib.load(model_path)

def word_char(inputs):
    # Tokenize the input text into individual characters
    return list(inputs)

def predict_password_strength(password):
    # Load the XGBoost model and the TfidfVectorizer
    model = load_xgboost_model('xgboost_model.joblib')
    vect = joblib.load('tfidf_vectorizer.joblib')

    # Transform the input password into a dataframe
    password_df = pd.DataFrame([password], columns=['password'])

    # Load the TfidfVectorizer with the correct tokenizer and transform the password
    vect.tokenizer = word_char
    password_tfidf = vect.transform(password_df['password'])

    # Make the prediction using the loaded XGBoost model
    strength_prediction = model.predict(password_tfidf)

    return strength_prediction[0]
