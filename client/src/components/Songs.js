import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";
import SongList from "../components/SongList";
import "../Styles/songs.css";
import Spline from "@splinetool/react-spline";

function Songs() {
  const location = useLocation();
  const playlistName = location.state?.playlistName || "Unknown Playlist";
  const [songlist, setSonglist] = useState(location.state?.trackItems || []);
  const [analyzedSongs, setAnalyzedSongs] = useState([]);
  const [removals, setRemovals] = useState([]);
  const [firstClick, setFirstClick] = useState(false);
  const playlistId = location.state?.playlistID || undefined;

  const analyzePlaylist = async () => {
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

  const toggleRemoval = (trackId, isChecked) => {
    setRemovals((prevRemovals) =>
      isChecked
        ? [...prevRemovals, trackId]
        : prevRemovals.filter((id) => id !== trackId)
    );
  };

  const removeOutliers = async () => {
    try {
      const trackUris = removals.map((trackId) => ({
        uri: `spotify:track:${trackId}`
      }));

      const response = await axios.delete("http://localhost:5000/remove-tracks", {
        data: {
          playlist_id: playlistId,
          tracks: trackUris
        },
        withCredentials: true
      });

      if (response.status === 200) {
        // Filter out from 'analyzedSongs' by matching 'song.id'
        const filteredAnalyzedSongs = analyzedSongs.filter(
          (song) => !removals.includes(song.id)
        );

        // Filter out from 'songlist' by matching 'song.track.id'
        const filteredSonglist = songlist.filter(
          (song) => !removals.includes(song.track.id)
        );

        setAnalyzedSongs(filteredAnalyzedSongs);
        setSonglist(filteredSonglist);
        setRemovals([]);
      } else {
        console.error("Failed to remove tracks:", response.data);
      }
    } catch (error) {
      console.error("Error in removing tracks:", error);
    }
  };

  return (
    /** 
     * Parent container that positions the Spline background 
     * and the main content. 
     */
    <div
      style={{
        position: "relative",
        width: "100%",
        height: "100vh",
        overflow: "hidden"
      }}
    >
      {/* Full-page Spline background */}
      <Spline
        scene="https://prod.spline.design/SItQV7KFk4UJ8zJ3/scene.splinecode"
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          zIndex: 0
        }}
      />

      {/* Your main app content above the Spline background */}
      <div className="container" style={{ position: "relative", zIndex: 1 }}>
        <h1>Playlist: {playlistName}</h1>

        <div className="songlist-container">
          <SongList songlist={songlist} />
        </div>

        <button
          className="cleanButton"
          onClick={() => analyzePlaylist(playlistId)}
        >
          Clean Playlist
        </button>

        {firstClick && (
          <div className="outlierPopup">
            <h2>Outliers Detected:</h2>
            {analyzedSongs.length > 0 ? (
              <div>
                <ul>
                  {analyzedSongs.map((song, index) => (
                    <li key={song.id || index}>
                      <input
                        className="checkbox"
                        type="checkbox"
                        onChange={(e) =>
                          toggleRemoval(song.id, e.target.checked)
                        }
                      />
                      {song.name} by {song.artist}
                    </li>
                  ))}
                </ul>
                <button className="outlierButton" onClick={removeOutliers}>
                  Remove Outliers
                </button>
              </div>
            ) : (
              <div id="none">None</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default Songs;
