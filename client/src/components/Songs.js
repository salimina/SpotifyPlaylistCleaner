import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";

function Songs() {
    const location = useLocation();
    const playlistName = location.state?.playlistName || "Unknown Playlist";
    const [songlist, setSonglist] = useState(location.state?.trackItems || [])
    console.log("Location State in Songs:", location.state);
    const playlistId = location.state?.playlistID || undefined;
    const [analyzedSongs, setAnalyzedSongs] = useState([]); // Songs with removal predictions
    const [removals, setRemovals] = useState([]);
    const [firstClick, setFirstClick] = useState(false);

const analyzePlaylist = async () => {
    console.log("Invoking analyzePlaylist with playlistId:", playlistId);
    try {
        const response = await axios.post(
            "http://localhost:5000/analyze-playlist",
            { playlist_id: playlistId },
            { withCredentials: true }
        );
        setAnalyzedSongs(response.data.tracks);
        setFirstClick(true);
    } catch (error) {
        console.error("Error analyzing playlist:", error);
    }
};

useEffect(() => {
    console.log("Updated removals:", removals);
}, [removals]);


const toggleRemoval = (songId, isChecked) => {
    setRemovals((prevRemovals) =>
        isChecked ? [...prevRemovals, songId] : prevRemovals.filter((id) => id !== songId) 
    );
};


const removeOutliers = async () => {
    try {
        // Make sure the removals array contains valid Spotify track URIs
        const trackUris = removals.map(trackId => ({
            uri: `spotify:track:${trackId}`
        }));

        const response = await axios.delete("http://localhost:5000/remove-tracks", {
            data: {
                playlist_id: playlistId, // Pass the playlist ID
                tracks: trackUris         // Send the formatted tracks array
            },
            withCredentials: true
        });

        if (response.status === 200) {
            console.log("Tracks removed successfully.");
            setRemovals([]);
            const filteredAnalyzedSongs = analyzedSongs.filter((track) => !removals.includes(track.id));

            // Filter out the removed tracks from songlist
            const filteredSonglist = songlist.filter((track) => !removals.includes(track.id));
        
            // Optionally, update the state with the new filtered arrays
            setAnalyzedSongs(filteredAnalyzedSongs);
            setSonglist(filteredSonglist);
        } else {
            console.error("Failed to remove tracks:", response.data);
        }
    } catch (error) {
        console.error("Error in removing tracks:", error);
    }
};

    // useEffect(() => {

    //     // Log songs with missing or invalid data
    //     songlist.forEach((song, index) => {
    //         console.log("songs:", song)
    //         if (!song?.track?.name) {
    //             console.log(`Song at index ${index} is missing a name or track object:`, song);
    //         }
    //     });
    // }, [songlist]);
      

    return (
        <div>
            <h1>Playlist: {playlistName}</h1>
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
                {firstClick && (
                    <div>
                        <h2>Outliers Detected:</h2>
                        {analyzedSongs.length > 0 ? (
                            <div>
                                <ul>
                                    {analyzedSongs.map((song, index) => (
                                        <li key={index}>
                                            <input type="checkbox" onChange={(e) => (toggleRemoval(song.id, e.target.checked))} />
                                            {song.name} by {song.artist}
                                        </li>
                                    ))}
                                </ul>
                                <button onClick={removeOutliers}>Remove Outliers</button>
                            </div>
                        ) : (
                            <div>None</div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

export default Songs;
