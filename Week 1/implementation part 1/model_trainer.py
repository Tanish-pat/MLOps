from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib
import os

def train_model(df, preprocessor):
    # Vectorization
    vectorizer = CountVectorizer(analyzer=preprocessor.tokenize)
    bow_transformer = vectorizer.fit(df["message"])
    messages_bow = bow_transformer.transform(df["message"])

    # TF-IDF Transformation
    tfidf_transformer = TfidfTransformer().fit(messages_bow)
    messages_tfidf = tfidf_transformer.transform(messages_bow)

    # Train Naive Bayes model
    model = MultinomialNB().fit(messages_tfidf, df["label"])

    # Save artifacts
    os.makedirs("artifacts", exist_ok=True)
    joblib.dump(vectorizer, "artifacts/vectorizer.pkl")
    joblib.dump(tfidf_transformer, "artifacts/tfidf_transformer.pkl")
    joblib.dump(model, "artifacts/spam_model.pkl")

    return model, messages_tfidf

def evaluate_model(model, X, y):
    predictions = model.predict(X)
    accuracy = accuracy_score(y, predictions)
    return accuracy
