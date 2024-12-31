import React from "react";
import "../Styles/homepage.css";

function HomePage() {
  const handleLogin = () => {
    // Just direct the browser to Flask’s /login route
    window.location.href = "http://localhost:5000/login";
  };

  return (
    <div className="container">
      <h1>Welcome to Spotify Playlist Cleaner</h1>
      <p>Log in to manage and clean up your playlists.</p>
      <button onClick={handleLogin}>Log in with Spotify</button>
    </div>
  );
}

export default HomePage;
