import { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";

import MapView from "../components/MapView";
import InfoPanel from "../components/InfoPanel";
import Loader from "../components/Loader";
import Particles from "../components/Particles";
import Navbar from "../components/Navbar";

export default function MapPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showOverlay, setShowOverlay] = useState(true);

  const BASE_URL = import.meta.env.VITE_BACKEND_URL;

  const handleClick = async (latlng) => {
    setLoading(true);
    setData(null);

    try {
      const res = await axios.get(
        `${BASE_URL}/analysis?lat=${latlng.lat}&lon=${latlng.lng}`
      );
      setData(res.data);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div style={{ position: "relative", height: "100vh", width: "100%" }}>

      {/* 🧭 NAVBAR */}
      <Navbar />

      {/* ✨ PARTICLES */}
      <Particles />

      {/* 🔥 MAIN LAYOUT */}
      <div style={{ display: "flex", height: "100%" }}>

        {/* 🌍 MAP */}
        <motion.div
          style={{
            width: data ? "70%" : "100%",
            height: "100%",
            transition: "width 0.4s ease"
          }}
        >
          <MapView onMapClick={handleClick} />
        </motion.div>

        {/* 📊 PANEL */}
        {data && (
          <div
            style={{
              width: "30%",
              height: "100%",
              background: "rgba(15,23,42,0.85)",
              backdropFilter: "blur(10px)",
              overflowY: "auto",
              padding: "10px"
            }}
          >
            <InfoPanel data={data} />
          </div>
        )}
      </div>

      {/* 🔥 HERO OVERLAY */}
      {showOverlay && (
        <motion.div
          initial={{ opacity: 1 }}
          animate={{ opacity: showOverlay ? 1 : 0 }}
          transition={{ duration: 0.6 }}
          style={overlayStyle}
        >
          <motion.div
            initial={{ y: 40, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
            style={{ textAlign: "center" }}
          >
            <h1 style={titleStyle}>🌍 EcoAir Insight</h1>

            <p style={{ opacity: 0.8, marginBottom: "20px" }}>
              AI-powered air quality intelligence across India
            </p>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setShowOverlay(false)}
              style={buttonStyle}
            >
              Explore Map →
            </motion.button>
          </motion.div>
        </motion.div>
      )}

      {/* 🔄 LOADER */}
      {loading && <Loader />}
    </div>
  );
}

/* 🎨 STYLES */

const overlayStyle = {
  position: "absolute",
  top: 0,
  left: 0,
  width: "100%",
  height: "100%",

  display: "flex",
  justifyContent: "center",
  alignItems: "center",

  background: "rgba(15, 23, 42, 0.6)",
  backdropFilter: "blur(6px)",

  zIndex: 999,
};

const titleStyle = {
  fontSize: "2.8rem",
  fontWeight: "600",
  color: "#e2e8f0",
  marginBottom: "10px",
};

const buttonStyle = {
  padding: "10px 20px",
  background: "#38bdf8",
  border: "none",
  borderRadius: "8px",
  cursor: "pointer",
  fontSize: "1rem",
  color: "#0f172a",
  fontWeight: "bold",
};