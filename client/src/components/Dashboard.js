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
  


    async function displaySongs(tracksHref) {
      console.log("Fetching all tracks from:", tracksHref);
  
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
              console.log(`Fetched ${response.data.items.length} tracks, total: ${allTracks.length}`);
  
              nextUrl = response.data.next; // Update next URL from the response
          }
  
          setSongs(allTracks); // Save all tracks to state
          console.log("All tracks fetched:", allTracks);
  
          // Navigate to Songs page and pass all tracks
          navigate("/songs", { state: { trackItems: allTracks } });
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
