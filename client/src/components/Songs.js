import React, { useEffect } from "react";
import { useLocation } from "react-router-dom";

function Songs() {
    const location = useLocation();
    const songlist = location.state?.trackItems || []; // Get trackItems from location state

    useEffect(() => {
        console.log("songlist passed to Songs component:", songlist);
    }, [songlist]); // Logs whenever songlist changes

    return (
        <div>
            <h1>Song List</h1>
            <ul>
                {songlist.map((song, index) => (
                    <li key={index}>{song.track.name} by {song.track.artists[0].name}</li> // Assuming each track has a "track.name"
                ))}
            </ul>
        </div>
    );
}

export default Songs;
