import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Dashboard() {
  const [playlists, setPlaylists] = useState([]);
  const [audioFeatures, setAudioFeatures] = useState([]); // Store audio features for songs
  const token = localStorage.getItem("spotify_token");
  const navigate = useNavigate();

  const [userId, setUserId] = useState(null);

  useEffect(() => {
      if (!token) {
        console.error("Token not found. Redirecting to home.");
        window.location.href = "/";
      } else {
        // Fetch current user's profile
        axios
          .get("https://api.spotify.com/v1/me", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          })
          .then((response) => {
            setUserId(response.data.id); // Save the user ID
          })
          .catch((error) => console.error("Error fetching user profile:", error));
  
        // Fetch playlists
        axios
          .get(`http://localhost:5000/playlists?token=${token}`)
          .then((response) => {
            setPlaylists(response.data.items || []);
          })
          .catch((error) => console.error("Error fetching playlists:", error));
      }
    }, [token]);
  


    async function displaySongs(tracksHref, playlistId) {
      const token = localStorage.getItem("spotify_token");
      let allTracks = [];
      let nextUrl = tracksHref;
  
      try {
          // Fetch tracks page by page
          while (nextUrl) {
              const response = await axios.get(nextUrl, {
                  headers: {
                      Authorization: `Bearer ${token}`, // Include the Spotify token
                  },
              });
  
              allTracks = allTracks.concat(response.data.items); // Add current page of tracks
  
              nextUrl = response.data.next; // Update next URL from the response
          }
  
          console.log("All Tracks:", allTracks);
          console.log("Navigating with Playlist ID:", playlistId);
  
          navigate("/songs", { state: { trackItems: allTracks, playlistID: playlistId }});
          
      } catch (error) {
          console.error("Error fetching tracks:", error);
      }
  }
    
  
  
  return (
    <div className="dashboard">
      <h1>Your Playlists</h1>
      <ul>
        {playlists.map((playlist) => (playlist.owner.id == userId) && (
          <li key={playlist.id}>
            {playlist.name}{" "}
            <div>
            <img
              key={playlist.index}
              src={playlist.images[0].url}
              alt={`${playlist.name} cover`}
              style={{ width: "100px", height: "100px", marginRight: "10px" }}
            />
          </div>
            <button onClick={() => {
              displaySongs(playlist.tracks.href, playlist.id)
              }}>
              View Songs
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
