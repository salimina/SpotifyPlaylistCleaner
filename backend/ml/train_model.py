import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
import joblib

def train_model():
    """
    Train a Random Forest model to predict song removal.
    """
    # Generate synthetic data
    data = pd.DataFrame({
        "popularity": [50, 30, 10, 80, 25, 60, 20, 90, 40, 15],
        "age": [2, 5, 10, 1, 8, 3, 12, 1, 6, 15],
        "avg_playlist_popularity": [60, 55, 40, 75, 45, 70, 50, 85, 65, 30],
        "relative_popularity": [50 - 60, 30 - 55, 10 - 40, 80 - 75, 25 - 45,
                                60 - 70, 20 - 50, 90 - 85, 40 - 65, 15 - 30],
        "genre_alignment_score": [0.8, 0.3, 0.1, 1.0, 0.2, 0.9, 0.0, 0.7, 0.5, 0.4],
        "genre": ["pop", "rock", "pop", "jazz", "rock", "pop", "hip-hop", "jazz", "hip-hop", "rock"],
        "label": [0, 1, 1, 0, 1, 0, 1, 0, 0, 1],
    })

    # One-hot encode genres
    encoder = OneHotEncoder()
    genre_encoded = encoder.fit_transform(data[["genre"]]).toarray()
    genre_columns = encoder.get_feature_names_out(["genre"])
    genre_df = pd.DataFrame(genre_encoded, columns=genre_columns)

    # Combine all features
    features = pd.concat([data[["popularity", "age", "avg_playlist_popularity", "relative_popularity", "genre_alignment_score"]], genre_df], axis=1)
    labels = data["label"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    # Train Random Forest model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

    # Save the model and encoder
    joblib.dump(model, "ml/song_removal_model.pkl")
    joblib.dump(encoder, "ml/genre_encoder.pkl")
    print("Model and encoder saved to ml/")

if __name__ == "__main__":
    train_model()
