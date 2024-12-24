import React from "react";

function HomePage() {
  const login = () => {
    // Redirect to the Flask backend for Spotify login
    console.log("Redirecting to login..."); // Debugging
    window.location.href = "http://localhost:5000/login";
  };

  return (
    <div className="container">
      <h1>Welcome to Spotify Playlist Cleaner</h1>
      <p>Log in to manage and clean up your playlists.</p>
      <button onClick={login}>Log in with Spotify</button>
    </div>
  );
}

export default HomePage;
