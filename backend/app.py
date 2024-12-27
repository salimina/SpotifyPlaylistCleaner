from flask import Flask, request, jsonify
from flask_cors import CORS
from ml.data_fetch import fetch_playlist_tracks_with_metrics
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="playlist-read-private user-library-read"
)

print(f"Authorized Scopes: {sp_oauth.scope}")

@app.route('/login')
def login():
    """Redirect user to Spotify login."""
    try:
        auth_url = sp_oauth.get_authorize_url()
        print(f"Auth URL: {auth_url}")  # Debugging
        return redirect(auth_url)
    except Exception as e:
        print(f"Error in /login: {e}")  # Debugging
        return jsonify({"error": str(e)}), 500


@app.route('/callback')
def callback():
    """Handle Spotify OAuth callback."""
    try:
        code = request.args.get('code')
        token_info = sp_oauth.get_access_token(code)

        access_token = token_info.get('access_token')
        refresh_token = token_info.get('refresh_token')

        # Print the granted scopes for debugging
        print(f"Granted Scopes: {token_info.get('scope')}")

        # Save refresh_token for future use
        if refresh_token:
            with open("refresh_token.txt", "w") as f:
                f.write(refresh_token)

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "scopes": token_info.get('scope')
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
def refresh_access_token():
    """Refresh the Spotify access token using the refresh token."""
    try:
        with open("refresh_token.txt", "r") as f:
            refresh_token = f.read().strip()

        print(f"Using refresh token: {refresh_token}")  # Debugging
        token_info = sp_oauth.refresh_access_token(refresh_token)
        new_access_token = token_info.get("access_token")
        print("Access token refreshed:", new_access_token)

        return new_access_token
    except FileNotFoundError:
        print("Refresh token file not found. Please log in again.")
        return None
    except Exception as e:
        print(f"Error refreshing access token: {e}")
        return None



@app.route('/playlists', methods=['GET'])
def get_playlists():
    token = request.args.get('token')
    sp = Spotify(auth=token)
    playlists = sp.current_user_playlists()
    return jsonify(playlists)

@app.route('/audio-features', methods=['GET'])
def get_audio_features():
    """Fetch audio features for a list of track IDs."""
    try:
        token = request.args.get('token')
        track_ids = request.args.get('track_ids')  # Comma-separated track IDs
        if not track_ids:
            return jsonify({"error": "No track IDs provided"}), 400
        sp = Spotify(auth=token)
        audio_features = sp.audio_features(track_ids.split(','))
        return jsonify(audio_features)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/recently-played', methods=['GET'])
def get_recently_played():
    """Fetch recently played tracks for the user."""
    try:
        token = request.args.get('token')
        sp = Spotify(auth=token)
        recently_played = sp.current_user_recently_played(limit=50)
        return jsonify(recently_played)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/recently-played-in-playlist', methods=['GET'])
def get_recently_played_in_playlist():
    """Fetch recently played tracks that are part of a specific playlist."""
    try:
        token = request.args.get('token')
        playlist_id = request.args.get('playlist_id')
        if not playlist_id:
            return jsonify({"error": "Playlist ID not provided"}), 400

        sp = Spotify(auth=token)

        # Fetch tracks in the playlist
        playlist_tracks = sp.playlist_tracks(playlist_id)
        playlist_track_ids = {item['track']['id'] for item in playlist_tracks['items']}

        # Fetch recently played tracks
        recently_played = sp.current_user_recently_played(limit=50)
        recently_played_ids = {item['track']['id'] for item in recently_played['items']}

        # Find intersection
        recently_played_in_playlist = playlist_track_ids.intersection(recently_played_ids)
        return jsonify({"recently_played_in_playlist": list(recently_played_in_playlist)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/track/<track_id>', methods=['GET'])
def get_track(track_id):
    """Fetch details for a specific track by ID."""
    try:
        token = request.args.get('token')
        sp = Spotify(auth=token)
        track = sp.track(track_id)
        return jsonify(track)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/playlist-tracks', methods=['GET'])
def get_playlist_tracks():
    """Fetch all tracks in a specific playlist."""
    try:
        token = request.args.get('token')
        playlist_id = request.args.get('playlist_id')
        if not playlist_id:
            return jsonify({"error": "Playlist ID not provided"}), 400

        sp = Spotify(auth=token)

        # Fetch all tracks in the playlist
        playlist_tracks = sp.playlist_tracks(playlist_id)
        return jsonify(playlist_tracks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/detect-outlier-songs/<playlist_id>", methods=["GET"])
def detect_outlier_songs(playlist_id):
    """Detect outlier songs in a playlist."""
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Authorization token is missing"}), 401

    token = token.replace("Bearer ", "")  # Remove "Bearer " prefix if present

    try:
        # Check if token works
        sp = Spotify(auth=token)
        sp.current_user()  # Test if the token is valid

    except Exception as e:
        print("Access token expired or invalid:", e)
        print("Refreshing token...")
        token = refresh_access_token()
        if not token:
            return jsonify({"error": "Failed to refresh access token"}), 401

    try:
        # Fetch playlist tracks with metrics
        user_id = 1234  # Replace with actual user ID if applicable
        tracks = fetch_playlist_tracks_with_metrics(playlist_id, user_id, token)

        # Return tracks as JSON
        return jsonify(tracks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
if __name__ == '__main__':
    app.run(port=5000)
