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
        return jsonify(token_info)  # Returns access token and other details
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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


if __name__ == '__main__':
    app.run(port=5000)
