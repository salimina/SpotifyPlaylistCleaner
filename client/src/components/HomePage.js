import React from "react";
import "../Styles/homepage.css";
import Spline from "@splinetool/react-spline";

function HomePage() {
  const handleLogin = () => {
    // Just direct the browser to Flask’s /login route
    window.location.href = "http://localhost:5000/login";
  };

  return (
    <div style={{ position: "relative", width: "100vw", height: "100vh", overflow: "hidden" }}>

      <Spline
        scene="https://prod.spline.design/SItQV7KFk4UJ8zJ3/scene.splinecode"
        style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%" , zIndex: 1}}
      />

      {/* Foreground content */}
      <div className="container" style={{ position: "relative", zIndex: 1 }}>
        <h1>Welcome to Spotify Playlist Cleaner</h1>
        <p>Log in to manage and clean up your playlists.</p>
        <button onClick={handleLogin}>Log in with Spotify</button>
      </div>
    </div>
  );
}

export default HomePage;
