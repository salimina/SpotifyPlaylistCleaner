import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

function Songs() {
    const location = useLocation();
    const songlist = location.state?.trackItems || []; // Get trackItems from location state
    console.log("Location State in Songs:", location.state);
    const playlistId = location.state?.playlistID || undefined;
    const [outlierSongs, setOutlierSongs] = useState([]); // State for outlier songs

    useEffect(() => {

        // Log songs with missing or invalid data
        songlist.forEach((song, index) => {
            if (!song?.track?.name) {
                console.log(`Song at index ${index} is missing a name or track object:`, song);
            }
        });
    }, [songlist]);

    const detectOutlierSongs = async () => {
        const token = localStorage.getItem("spotify_token"); // Retrieve token from local storage

        if (!token) {
            console.error("Token not found!");
            return;
        }

        try {
            const response = await fetch(`http://localhost:5000/detect-outlier-songs/${playlistId}`, {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${token}`, // Pass the token in the Authorization header
                },
            });
            console.log("reached");

            const data = await response.json();
            console.log("Outlier Detection Response:", data);
            setOutlierSongs(data); // Update the state with detected outlier songs
        } catch (error) {
            console.error("Error detecting outlier songs:", error);
        }
    };

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
                        detectOutlierSongs(playlistId);
                    }}
                >
                    Clean Playlist
                </button>
            </div>
            <div>
                <h2>Outlier Songs</h2>
                {outlierSongs.length > 0 ? (
                    <ul>
                        {outlierSongs.map((song, index) => (
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
