from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def preprocess_and_weight_features(tracks):
    """
    Preprocess Spotify features and apply weighting to user-specific metrics.
    """
    df = pd.DataFrame(tracks)

    # Normalize Spotify features
    scaler = MinMaxScaler()
    spotify_features = [
        "danceability", "energy", "valence", "acousticness", 
        "loudness", "tempo", "speechiness", "instrumentalness", "liveness"
    ]
    df[spotify_features] = scaler.fit_transform(df[spotify_features])

    # Add mock listens/skips weighting for now
    if "listens" in df.columns and "skips" in df.columns:
        user_metrics = ["listens", "skips"]
        df[user_metrics] = scaler.fit_transform(df[user_metrics])
        df["weighted_listens"] = df["listens"] * 2
        df["weighted_skips"] = df["skips"] * -1
    else:
        df["weighted_listens"] = 0
        df["weighted_skips"] = 0

    # Combined feature adjustment
    df["adjusted_feature"] = (
        df["danceability"] +
        df["energy"] +
        df["valence"] +
        df["weighted_listens"] +
        df["weighted_skips"]
    )

    return df



def cluster_and_identify_outliers(tracks):
    """
    Cluster Spotify tracks and identify outliers based on distance from cluster centers.
    """
    df = preprocess_and_weight_features(tracks)

    # Use Spotify features for clustering
    spotify_features = [
        "danceability", "energy", "valence", "acousticness", 
        "loudness", "tempo", "speechiness", "instrumentalness", "liveness"
    ]
    kmeans = KMeans(n_clusters=2, random_state=42)
    df["cluster"] = kmeans.fit_predict(df[spotify_features])  # Add cluster column

    # Calculate distance to cluster centers
    def calculate_distance(row):
        cluster_center = kmeans.cluster_centers_[row["cluster"]]
        return sum((row[spotify_features] - cluster_center) ** 2)

    df["distance_to_centroid"] = df.apply(calculate_distance, axis=1)  # Add distance column

    # Set outliers based on distance threshold
    outlier_threshold = df["distance_to_centroid"].quantile(0.8)
    df["is_outlier"] = df["distance_to_centroid"] > outlier_threshold

    return df