import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import HomePage from "./components/HomePage";
import Dashboard from "./components/Dashboard";
import Callback from "./components/Callback"; 
import Songs from "./components/Songs";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/callback" element={<Callback />} /> 
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/songs" element={<Songs />} />
      </Routes>
    </Router>
  );
}

export default App;
