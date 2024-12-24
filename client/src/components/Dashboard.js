import React, { useEffect, useState } from "react";
import axios from "axios";

function Dashboard() {
  const [playlists, setPlaylists] = useState([]);
  const [selectedPlaylist, setSelectedPlaylist] = useState(null); // Store selected playlist
  const [songs, setSongs] = useState([]); // Store songs in the selected playlist
  const [audioFeatures, setAudioFeatures] = useState([]); // Store audio features for songs
  const token = localStorage.getItem("spotify_token");

  // Fetch user playlists on load
  useEffect(() => {
    if (!token) {
      console.error("Token not found. Redirecting to home.");
      // window.location.href = "/"; // Uncomment to redirect to home if no token
    } else {
      // Fetch playlists
      axios
        .get(`http://localhost:5000/playlists?token=${token}`)
        .then((response) => setPlaylists(response.data.items || []))
        .catch((error) => console.error("Error fetching playlists:", error));
    }
  }, [token]);

  // Fetch songs when a playlist is selected
  useEffect(() => {
    if (selectedPlaylist) {
      // Fetch tracks in the selected playlist
      axios
        .get(`http://localhost:5000/playlists/${selectedPlaylist}?token=${token}`)
        .then((response) => {
          const trackItems = response.data.items || [];
          setSongs(trackItems);

          // Extract track IDs and fetch audio features
          const trackIds = trackItems.map((item) => item.track.id).join(",");
          return axios.get(`http://localhost:5000/audio-features?token=${token}&track_ids=${trackIds}`);
        })
        .then((response) => setAudioFeatures(response.data || []))
        .catch((error) => console.error("Error fetching songs or audio features:", error));
    }
  }, [selectedPlaylist, token]);

  return (
    <div className="dashboard">
      <h1>Your Playlists</h1>
      <ul>
        {playlists.map((playlist) => (
          <li key={playlist.id}>
            {playlist.name}{" "}
            <button onClick={() => setSelectedPlaylist(playlist.id)}>
              View Songs
            </button>
          </li>
        ))}
      </ul>

      {selectedPlaylist && (
        <>
          <h2>Selected Playlist: {playlists.find((p) => p.id === selectedPlaylist)?.name}</h2>
          <h3>Songs in Playlist</h3>
          <ul>
            {songs.map((item) => (
              <li key={item.track.id}>
                {item.track.name} by{" "}
                {item.track.artists.map((artist) => artist.name).join(", ")}
              </li>
            ))}
          </ul>

          <h3>Audio Features</h3>
          <ul>
            {audioFeatures.map((feature, index) => (
              <li key={index}>
                {songs[index]?.track.name} - Danceability: {feature.danceability}, Energy: {feature.energy}, Valence: {feature.valence}
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default Dashboard;
