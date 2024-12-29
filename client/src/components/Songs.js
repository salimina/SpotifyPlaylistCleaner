import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";

function Songs() {
    const location = useLocation();
    const songlist = location.state?.trackItems || []; // Get trackItems from location state
    console.log("Location State in Songs:", location.state);
    const playlistId = location.state?.playlistID || undefined;
    const [analyzedSongs, setAnalyzedSongs] = useState([]); // Songs with removal predictions

    const analyzePlaylist = async () => {
        try {
          const response = await axios.post(
            "http://localhost:5000/analyze-playlist",
            { playlist_id: playlistId },
            { withCredentials: true }
          );
          setAnalyzedSongs(response.data);
        } catch (error) {
          console.error("Error analyzing playlist:", error);
        }
      };

    useEffect(() => {

        // Log songs with missing or invalid data
        songlist.forEach((song, index) => {
            if (!song?.track?.name) {
                console.log(`Song at index ${index} is missing a name or track object:`, song);
            }
        });
    }, [songlist]);
      

    return (
        <div>
            <h1>Song List</h1>
            <ul>
                {songlist.map((song, index) => {
                    // Ensure song and song.track are valid
                    if (!song?.track) {
                        return null; // Skip this song
                    }

                    // Render the song details
                    return (
                        <li key={index}>
                            {song.track.name || "Unnamed Song"} by {song.track.artists[0]?.name || "Unknown Artist"}
                        </li>
                    );
                })}
            </ul>
            <div>
                <button
                    onClick={() => {
                        analyzePlaylist(playlistId);
                    }}
                >
                    Clean Playlist
                </button>
            </div>
            <div>
                <h2>Outlier Songs</h2>
                {analyzedSongs.length > 0 ? (
                    <ul>
                        {analyzedSongs.map((song, index) => (
                            <li key={index}>
                                {song.track.name || "Unnamed Song"} by {song.track.artists[0]?.name || "Unknown Artist"}
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>No outliers detected yet.</p>
                )}
            </div>
        </div>
    );
}

export default Songs;
