from flask import Flask, request, jsonify, redirect, session
from flask_cors import CORS
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
from dotenv import load_dotenv
from ml.predict import predict_song_removal  # Import the function
import os
import numpy as np
from datetime import datetime


load_dotenv()

app = Flask(__name__)

# Enable CORS so your front-end (different domain/port) can send cookies
CORS(app, supports_credentials=True)

# Make sure you have a real secret key in your .env (FLASK_SECRET_KEY="something random")
app.secret_key = os.getenv("FLASK_SECRET_KEY") or "SUPER_SECRET_FALLBACK"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="playlist-read-private playlist-modify-public playlist-modify-private user-library-read"
)

print(f"Authorized Scopes: {sp_oauth.scope}")


# -----------------------------------------------------------------------------
# 1. OAUTH LOGIN + CALLBACK
# -----------------------------------------------------------------------------

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
    """
    Handle Spotify OAuth callback:
    - Exchange the 'code' for an access token.
    - Store tokens in the Flask session.
    """
    try:
        code = request.args.get('code')
        if not code:
            return jsonify({"error": "No code provided by Spotify"}), 400

        token_info = sp_oauth.get_access_token(code)

        # Extract tokens
        access_token = token_info.get('access_token')
        refresh_token = token_info.get('refresh_token')

        # Store tokens in the session
        session['spotify_token'] = access_token
        session['spotify_refresh_token'] = refresh_token

        # Option A: Return JSON if your front-end expects it:
        # return jsonify({
        #     "access_token": access_token,
        #     "refresh_token": refresh_token,
        #     "scopes": token_info.get('scope')
        # })

        # Option B: Redirect to your React app after successful auth:
        return redirect("http://localhost:3000/dashboard")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def refresh_access_token():
    """Refresh the Spotify access token using the refresh token stored in the session."""
    try:
        refresh_token = session.get("spotify_refresh_token")
        if not refresh_token:
            print("No refresh token in session. Please log in again.")
            return None

        print(f"Using refresh token: {refresh_token}")  # Debugging
        token_info = sp_oauth.refresh_access_token(refresh_token)
        new_access_token = token_info.get("access_token")
        print("Access token refreshed:", new_access_token)

        # Update the session with the new token
        session['spotify_token'] = new_access_token

        # If Spotify returned a new refresh token, update it too
        if 'refresh_token' in token_info:
            session['spotify_refresh_token'] = token_info['refresh_token']

        return new_access_token
    except Exception as e:
        print(f"Error refreshing access token: {e}")
        return None


def get_valid_spotify_client():
    """
    Helper function:
    Retrieves the user's token from session, attempts to validate it,
    refreshes if necessary, and returns a Spotipy client (Spotify object).
    """
    token = session.get('spotify_token')
    if not token:
        return None  # Means user not logged in or token missing

    try:
        sp = Spotify(auth=token)
        # Test if token is still valid
        sp.current_user()  # Will raise exception if invalid/expired
        return sp
    except Exception:
        # Token invalid or expired, try to refresh
        new_token = refresh_access_token()
        if not new_token:
            return None
        return Spotify(auth=new_token)


# -----------------------------------------------------------------------------
# 2. SESSION-BASED ENDPOINTS
# -----------------------------------------------------------------------------

@app.route("/me", methods=["GET"])
def get_user_profile():
    """
    Return the current user's Spotify profile using the session token.
    Called by the front-end to get userId, display name, etc.
    """
    sp = get_valid_spotify_client()
    if not sp:
        return jsonify({"error": "No valid token in session."}), 401

    try:
        profile = sp.current_user()
        return jsonify(profile)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/playlists", methods=["GET"])
def get_user_playlists():
    """
    Return the current user's playlists using the session token.
    Called by the front-end Dashboard to list user’s playlists.
    """
    sp = get_valid_spotify_client()
    if not sp:
        return jsonify({"error": "No valid token in session."}), 401

    try:
        playlists = sp.current_user_playlists()
        return jsonify(playlists)  # Should be an object like { items: [...] }
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/playlist-tracks", methods=["GET"])
def get_playlist_tracks():
    """
    Fetch all tracks from a given playlist using the session-based token.
    Expects ?playlist_id=<ID> from the front end.
    """
    sp = get_valid_spotify_client()
    if not sp:
        return jsonify({"error": "No valid token in session."}), 401

    playlist_id = request.args.get("playlist_id")
    if not playlist_id:
        return jsonify({"error": "playlist_id param missing"}), 400

    try:
        # If you want to fetch beyond 100 tracks, you'd iterate with offsets here.
        tracks = sp.playlist_tracks(playlist_id)
        return jsonify(tracks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/remove-tracks", methods=["DELETE"])
def remove_tracks_from_playlist():
    """
    Remove tracks from a Spotify playlist using the session-based token.
    Expects playlist_id and tracks (list of track URIs) in the request body.
    """
    print("Reached backend - remove-tracks endpoint.")
    sp = get_valid_spotify_client()
    if not sp:
        return jsonify({"error": "No valid token in session."}), 401

    data = request.json
    tracks = data.get("tracks")
    playlist_id = data.get("playlist_id")

    print(f"Received tracks: {tracks}")
    print(f"Received playlist_id: {playlist_id}")

    if not tracks or not playlist_id:
        return jsonify({"error": "Missing tracks or playlist_id"}), 400

    try:
        # Extract URIs from the track objects and pass them as strings
        track_uris = [track["uri"] for track in tracks]
        print(f"Track URIs to be removed: {track_uris}")

        # Use the Spotipy method to remove tracks from the playlist
        sp.playlist_remove_all_occurrences_of_items(playlist_id, track_uris)

        return jsonify({"message": "Tracks removed successfully"}), 200

    except Exception as e:
        # Log the error and the response from Spotify (if available)
        print(f"Error removing tracks: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/analyze-playlist", methods=["POST"])
def analyze_playlist():
    """
    Analyze a playlist using track-level, playlist-level, and genre alignment features.
    """
    sp = get_valid_spotify_client()
    if not sp:
        return jsonify({"error": "No valid token in session."}), 401

    playlist_id = request.json.get("playlist_id")
    if not playlist_id:
        return jsonify({"error": "Missing playlist_id"}), 400

    try:
        playlist_tracks = sp.playlist_tracks(playlist_id)
        all_popularity = []
        all_genres = []
        tracks = []

        for item in playlist_tracks["items"]:
            try:
                # Handle missing track data gracefully
                track = item.get("track", {})
                track_id = track.get("id", "unknown_id")
                name = track.get("name", "Unknown Song")
                popularity = track.get("popularity", 0)
                release_date = track.get("album", {}).get("release_date", "2000-01-01")
                release_year = int(release_date.split("-")[0])
                age = datetime.now().year - release_year

                # Handle missing artist data gracefully
                artist_data = track.get("artists", [{}])
                artist_id = artist_data[0].get("id", "unknown_artist_id")
                artist_name = artist_data[0].get("name", "Unknown Artist")

                # Fetch genres for the track's primary artist (handle missing artist info)
                genres = ["unknown"]
                if artist_id != "unknown_artist_id":
                    artist_info = sp.artist(artist_id)
                    genres = artist_info.get("genres", ["unknown"])

                genre = genres[0] if genres else "unknown"

                # Update playlist-level statistics
                all_popularity.append(popularity)
                all_genres.extend(genres)

                # Calculate features
                avg_playlist_popularity = (
                    sum(all_popularity) / len(all_popularity) if all_popularity else 0
                )
                relative_popularity = popularity - avg_playlist_popularity
                genre_alignment_score = sum(
                    1 for g in genres if g in Counter(all_genres).most_common(3)
                ) / 3

                features = [
                    popularity,
                    age,
                    avg_playlist_popularity,
                    relative_popularity,
                    genre_alignment_score,
                ]

                # Call prediction function
                remove = predict_song_removal(features, genre)


                if remove == 1:
                # Append the track to the results
                    tracks.append({
                        "id": track_id,
                        "name": name,
                        "artist": artist_name,
                        "remove": remove,
                    })
            except Exception as track_error:
                print(f"Error processing track: {track_error}")

        return jsonify({"tracks": tracks})

    except Exception as e:
        print("Error analyzing playlist:", e)
        return jsonify({"error": str(e)}), 500
    












if __name__ == '__main__':
    app.run(port=5000)
