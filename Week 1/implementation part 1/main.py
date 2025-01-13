from data_loader import load_data
from text_preprocessor import PreProcessText
from model_trainer import train_model, evaluate_model

if __name__ == "__main__":
    # Load data
    df = load_data("SMSSpamCollection.txt")

    # Preprocessing
    preprocessor = PreProcessText()

    # Train model
    model, messages_tfidf = train_model(df, preprocessor)

    # Evaluate model
    accuracy = evaluate_model(model, messages_tfidf, df["label"])
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
