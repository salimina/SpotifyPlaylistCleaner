import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
import joblib
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import numpy as np

def get_song_vector(lyrics, word2vec_model, vector_size=100):
    """Generate a vector representation for a song based on its lyrics."""
    tokens = word_tokenize(lyrics.lower())
    vectors = [word2vec_model.wv[word] for word in tokens if word in word2vec_model.wv]
    return np.mean(vectors, axis=0) if vectors else np.zeros(vector_size)

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
        "lyrics": [
            "I see trees of green red roses too",
            "Rocking all night long under the moon",
            "Love is in the air everywhere I look",
            "Smooth jazz rhythms soothe the soul",
            "Rock and roll dreams keep me alive",
            "Pop melodies dance through the air",
            "Hip-hop beats keep the city alive",
            "Cool jazz plays in the smoky lounge",
            "Rhythmic beats from the heart of the streets",
            "Rock anthems echo through the canyon"
        ],
        "label": [0, 1, 1, 0, 1, 0, 1, 0, 0, 1],
    })

    # Train Word2Vec model on lyrics
    tokenized_lyrics = [word_tokenize(lyrics.lower()) for lyrics in data["lyrics"]]
    word2vec_model = Word2Vec(sentences=tokenized_lyrics, vector_size=100, window=5, min_count=1, workers=4)

    # Compute Word2Vec vectors for each song
    data["word2vec"] = data["lyrics"].apply(lambda lyrics: get_song_vector(lyrics, word2vec_model))

    # One-hot encode genres
    encoder = OneHotEncoder()
    genre_encoded = encoder.fit_transform(data[["genre"]]).toarray()
    genre_columns = encoder.get_feature_names_out(["genre"])
    genre_df = pd.DataFrame(genre_encoded, columns=genre_columns)

    # Combine all features
    word2vec_features = pd.DataFrame(data["word2vec"].to_list(), columns=[f"w2v_{i}" for i in range(100)])
    features = pd.concat([
        data[["popularity", "age", "avg_playlist_popularity", "relative_popularity", "genre_alignment_score"]],
        genre_df,
        word2vec_features
    ], axis=1)
    labels = data["label"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    # Train Random Forest model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

    # Save the model, encoder, and Word2Vec model
    joblib.dump(model, "ml/song_removal_model.pkl")
    joblib.dump(encoder, "ml/genre_encoder.pkl")
    joblib.dump(word2vec_model, "ml/word2vec_model.pkl")
    print("Model, encoder, and Word2Vec model saved to ml/")

if __name__ == "__main__":
    train_model()
