import joblib
import numpy as np

# Load the trained model and encoder
model = joblib.load("ml/song_removal_model.pkl")
encoder = joblib.load("ml/genre_encoder.pkl")  # For encoding genres

def predict_song_removal(features, genre):
    """
    Predict whether a song should be removed.

    Parameters:
        - features: List of numerical features
          [popularity, age, avg_playlist_popularity, relative_popularity, genre_alignment_score]
        - genre: The primary genre of the song as a string (e.g., "pop", "rock")

    Returns:
        - 0 (keep) or 1 (remove)
    """

    # Encode the genre into a one-hot vector
    try:
        genre_encoded = encoder.transform([[genre]]).toarray()
    except Exception:
        # Handle unknown genres by using a zero vector
        genre_encoded = np.zeros((1, len(encoder.get_feature_names_out())))


    # Combine numerical features with encoded genre
    full_features = np.hstack([features, genre_encoded[0]])

    # Predict using the model
    full_features = np.array(full_features).reshape(1, -1)
    prediction = model.predict(full_features)
    return int(prediction[0])  # Return 0 (keep) or 1 (remove)
