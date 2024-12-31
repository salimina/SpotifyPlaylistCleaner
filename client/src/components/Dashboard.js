import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Dashboard() {
  const navigate = useNavigate();

  // Store user ID and playlists from the server
  const [userId, setUserId] = useState(null);
  const [playlists, setPlaylists] = useState([]);

  // On mount, fetch user profile and playlists from your Flask server (session-based)
  useEffect(() => {
    // 1. Fetch current user profile
    axios
      .get("http://localhost:5000/me", {
        withCredentials: true, // <--- critical to send session cookie
      })
      .then((response) => {
        setUserId(response.data.id);
      })
      .catch((error) => {
        console.error("Error fetching user profile:", error);
        // If 401, user not logged in; redirect to home (or login)
        if (error.response && error.response.status === 401) {
          window.location.href = "/";
        }
      });

    // 2. Fetch user playlists
    axios
      .get("http://localhost:5000/playlists", {
        withCredentials: true, // <--- again, must send the session cookie
      })
      .then((response) => {
        // Assuming your Flask route returns the raw Spotify JSON
        // e.g. { items: [...] }
        setPlaylists(response.data.items || []);
      })
      .catch((error) => {
        console.error("Error fetching playlists:", error);
      });
  }, []);

  // Fetch the tracks for a given playlist, using a server-based route
  async function displaySongs(playlistId, Name) {
    try {
      // Example: you might have a server route like `/playlist-tracks?playlist_id=xxx`
      const response = await axios.get(
        `http://localhost:5000/playlist-tracks?playlist_id=${playlistId}`,
        { withCredentials: true } // send session cookie
      );
      // Suppose your Flask route returns { items: [...] } or a similar structure
      const allTracks = response.data.items || [];
      console.log("All Tracks:", Name);

      // Navigate to /songs page, passing trackItems in location.state
      navigate("/songs", { state: { trackItems: allTracks, playlistID: playlistId, playlistName: Name} });
    } catch (error) {
      console.error("Error fetching tracks:", error);
    }
  }

  return (
    <div className="dashboard">
      <h1>Your Playlists</h1>
      <ul>
        {playlists.map((playlist) => (
          // Only show playlists owned by the user
          playlist.owner?.id === userId && (
            <li key={playlist.id}>
              <div>{playlist.name}</div>
              {playlist.images && playlist.images.length > 0 && (
                <img
                  src={playlist.images[0].url}
                  alt={`${playlist.name} cover`}
                  style={{ width: "100px", height: "100px", marginRight: "10px" }}
                />
              )}
              <button onClick={() => displaySongs(playlist.id, playlist.name)}>
                View Songs
              </button>
            </li>
          )
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
