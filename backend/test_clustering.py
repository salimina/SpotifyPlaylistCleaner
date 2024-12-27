from ml.data_fetch import fetch_audio_features  # Example of fetching real data if needed
from ml.clustering import preprocess_and_weight_features, cluster_and_identify_outliers

# Mock Data: Simulating Spotify audio features for testing
mock_tracks = [
    {"id": "track_1", "name": "Song A", "danceability": 0.8, "energy": 0.9, "valence": 0.7, "acousticness": 0.1, "loudness": -5.5, "tempo": 120, "speechiness": 0.05, "instrumentalness": 0.0, "liveness": 0.1, "listens": 50, "skips": 2},
    {"id": "track_2", "name": "Song B", "danceability": 0.3, "energy": 0.4, "valence": 0.2, "acousticness": 0.8, "loudness": -10, "tempo": 90, "speechiness": 0.1, "instrumentalness": 0.2, "liveness": 0.3, "listens": 20, "skips": 10},
    {"id": "track_3", "name": "Song C", "danceability": 0.7, "energy": 0.8, "valence": 0.6, "acousticness": 0.2, "loudness": -6, "tempo": 110, "speechiness": 0.05, "instrumentalness": 0.0, "liveness": 0.2, "listens": 40, "skips": 5},
    {"id": "track_4", "name": "Song D", "danceability": 0.4, "energy": 0.5, "valence": 0.3, "acousticness": 0.7, "loudness": -9, "tempo": 95, "speechiness": 0.08, "instrumentalness": 0.1, "liveness": 0.25, "listens": 10, "skips": 15}
]

if __name__ == "__main__":
    # Run clustering and outlier detection
    df = cluster_and_identify_outliers(mock_tracks)

    # Debugging: Check DataFrame columns
    print("Columns in DataFrame after clustering:", df.columns)

    # Print results
    print("Clustered Data:")
    print(df[["id", "name", "cluster", "distance_to_centroid", "is_outlier"]])

    print("\nOutliers:")
    print(df[df["is_outlier"]][["id", "name", "distance_to_centroid"]])