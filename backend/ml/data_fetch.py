import requests
from flask import request

def fetch_audio_features(track_id, token):
    """
    Fetch Spotify audio features for a specific track.
    """
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    print(f"Token received: {token}")
    print(f"URL: {url}")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    error_data = response.json()
    print(f"Error: {error_data}")

    if response.status_code == 200:
        data = response.json()
        
        # Extract relevant features
        return {
            "danceability": data["danceability"],
            "energy": data["energy"],
            "valence": data["valence"],
            "acousticness": data["acousticness"],
            "loudness": data["loudness"],
            "tempo": data["tempo"],
            "speechiness": data["speechiness"],
            "instrumentalness": data["instrumentalness"],
            "liveness": data["liveness"]
        }
    else:
        return None  # Handle error cases appropriately

# def get_user_metrics(user_id):
#     """
#     Mock function or database call to fetch user-specific metrics.
#     Replace with actual database query or API.
#     """
#     # Example: Mock data structure
#     return {
#         "track_id_1": {"listens": 10, "skips": 2},
#         "track_id_2": {"listens": 5, "skips": 10},
#     }

def fetch_playlist_tracks_with_metrics(playlist_id, user_id, token):
    """
    Fetch tracks from a Spotify playlist and include user-specific metrics.
    """
    # Fetch playlist data from Spotify API
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    user_metrics = []

    # Get user-specific metrics (mocked or from a database)
    # user_metrics = get_user_metrics(user_id)
    # print(f"User metrics reached: {user_metrics}")

    tracks = []
    for item in data.get("items", []):
        track = item["track"]
        features = fetch_audio_features(track["id"], token)  # Pass token dynamically
        print(f"reached features: {features}")
        listens = user_metrics.get(track["id"], {}).get("listens", 0)
        skips = user_metrics.get(track["id"], {}).get("skips", 0)

        tracks.append({
            "id": track["id"],
            "name": track["name"],
            "danceability": features["danceability"],
            "energy": features["energy"],
            "valence": features["valence"],
            "acousticness": features["acousticness"],
            "loudness": features["loudness"],
            "tempo": features["tempo"],
            "speechiness": features["speechiness"],
            "instrumentalness": features["instrumentalness"],
            "liveness": features["liveness"],
            "listens": listens,
            "skips": skips,
        })
    return tracks
