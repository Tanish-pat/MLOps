from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
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
    # model = MultinomialNB().fit(messages_tfidf, df["label"])

    X_train, X_test, y_train, y_test = train_test_split(messages_tfidf, df["label"], test_size=0.2, random_state=42)

    # Initialize the Multinomial Naive Bayes model
    mnb = MultinomialNB()

    # Define parameter grid
    param_grid = {
        'alpha': [0.1, 0.5, 1.0, 2.0],  # Different smoothing values
    }

    # Perform GridSearchCV
    grid_search = GridSearchCV(estimator=mnb, param_grid=param_grid, cv=5, scoring='accuracy', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    # Test the best model on the test set
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Save artifacts
    os.makedirs("artifacts", exist_ok=True)
    joblib.dump(vectorizer, "artifacts/vectorizer.pkl")
    joblib.dump(tfidf_transformer, "artifacts/tfidf_transformer.pkl")
    joblib.dump(best_model, "artifacts/spam_model.pkl")

    return best_model, messages_tfidf

def evaluate_model(model, X, y):
    predictions = model.predict(X)
    accuracy = accuracy_score(y, predictions)
    return accuracy
