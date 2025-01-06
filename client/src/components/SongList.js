import React, { useEffect, useState } from "react";

function SongList({ songlist }) {
    return (
        <ul>
            {songlist.map((song, index) => {
                if (!song?.track) {
                    return null;
                }
                return (
                    <li key={index}>
                        {song.track.name || "Unnamed Song"} by{" "}
                        {song.track.artists[0]?.name || "Unknown Artist"}
                    </li>
                );
            })}
        </ul>
    );
}

export default SongList;