import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Dashboard() {
  const [playlists, setPlaylists] = useState([]);
  const [selectedPlaylist, setSelectedPlaylist] = useState(null); // Store selected playlist
  const [songs, setSongs] = useState([]); // Store songs in the selected playlist
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
            console.log("Logged-in user ID:", response.data.id);
          })
          .catch((error) => console.error("Error fetching user profile:", error));
  
        // Fetch playlists
        axios
          .get(`http://localhost:5000/playlists?token=${token}`)
          .then((response) => {
            setPlaylists(response.data.items || []);
            console.log("Fetched playlists:", response.data.items);
          })
          .catch((error) => console.error("Error fetching playlists:", error));
      }
    }, [token]);
  


  function displaySongs(tracksHref) {
    console.log("Tracks link:", tracksHref);
    
    if (tracksHref) {
      // Fetch tracks using the provided href
      axios
        .get(tracksHref, {
          headers: {
            Authorization: `Bearer ${token}`, // Include the Spotify token
          },
        })
        .then((response) => {
          const trackItems = response.data.items || [];
          setSongs(trackItems);
          console.log("Tracks fetched:", trackItems);
          navigate("/songs", { state: { trackItems } });
        }).catch((error) => console.error("Error fetching tracks or audio features:", error));
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
              console.log("Button clicked for playlist ID:", playlist);
              displaySongs(playlist.tracks.href)
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
