import React, { useEffect } from "react";
import { useLocation } from "react-router-dom";

function Songs() {
    const location = useLocation();
    const songlist = location.state?.trackItems || []; // Get trackItems from location state

    useEffect(() => {
        console.log("songlist passed to Songs component:", songlist);

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
                        console.log(`Skipping song at index ${index}: Invalid track object`, song);
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
        </div>
    );
}

export default Songs;
