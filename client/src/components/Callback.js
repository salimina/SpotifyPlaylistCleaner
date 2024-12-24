import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Callback() {
  const navigate = useNavigate();

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");

    if (code) {
      console.log("Authorization code received:", code); // Debugging

      // Send the code to the Flask backend
      fetch(`http://localhost:5000/callback?code=${code}`)
        .then((response) => response.json())
        .then((data) => {
          if (data.access_token) {
            localStorage.setItem("spotify_token", data.access_token); // Save the token
            console.log("Token saved:", data.access_token); // Debugging
            navigate("/dashboard"); // Redirect to the dashboard
          } else {
            console.error("No access token received:", data);
            alert("Authentication failed. Please try again.");
            navigate("/"); // Redirect back to home
          }
        })
        .catch((error) => {
          console.error("Error during token exchange:", error);
          alert("Authentication failed. Please try again.");
          navigate("/"); // Redirect back to home
        });
    } else {
      console.error("No code found in URL. Redirecting to home.");
      navigate("/"); // Redirect back to home
    }
  }, [navigate]);

  return <p>Processing your login...</p>;
}

export default Callback;
