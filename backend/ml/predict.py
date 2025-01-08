import joblib
import numpy as np
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize

# Load the trained model, encoder, and Word2Vec model
model = joblib.load("ml/song_removal_model.pkl")
encoder = joblib.load("ml/genre_encoder.pkl")
word2vec = joblib.load("ml/word2vec_model.pkl")

def get_song_vector(lyrics, word2vec_model, vector_size=100):
    """Generate a vector representation for a song based on its lyrics."""
    tokens = word_tokenize(lyrics.lower())
    vectors = [word2vec_model.wv[word] for word in tokens if word in word2vec_model.wv]
    return np.mean(vectors, axis=0) if vectors else np.zeros(vector_size)

def predict_song_removal(features, genre, lyrics):
    """
    Predict whether a song should be removed.

    Parameters:
        - features: List of numerical features
          [popularity, age, avg_playlist_popularity, relative_popularity, genre_alignment_score]
        - genre: The primary genre of the song as a string
        - lyrics: The lyrics of the song as a string

    Returns:
        - 0 (keep) or 1 (remove)
    """

    # Encode the genre into a one-hot vector
    try:
        genre_encoded = encoder.transform([[genre]]).toarray()
    except Exception:
        genre_encoded = np.zeros((1, len(encoder.get_feature_names_out())))

    # Generate Word2Vec vector for the song's lyrics
    song_vector = get_song_vector(lyrics, word2vec)

    # Combine all features
    full_features = np.hstack([features, genre_encoded[0], song_vector])

    # Predict using the model
    full_features = np.array(full_features).reshape(1, -1)
    prediction = model.predict(full_features)
    return int(prediction[0])  # 0 = keep, 1 = remove
