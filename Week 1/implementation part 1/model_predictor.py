import joblib

class ModelPredictor:
    def __init__(self):
        self.vectorizer = joblib.load("artifacts/vectorizer.pkl")
        self.tfidf_transformer = joblib.load("artifacts/tfidf_transformer.pkl")
        self.model = joblib.load("artifacts/spam_model.pkl")

    def predict(self, message: str) -> str:
        bow = self.vectorizer.transform([message])
        tfidf = self.tfidf_transformer.transform(bow)
        return self.model.predict(tfidf)[0]
