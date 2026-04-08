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
    <Navbar />
    <div style={{ position: "relative" }}>
      {/* 🌍 MAP ALWAYS VISIBLE */}
      <motion.div
  initial={{ scale: 1.1, filter: "blur(10px)" }}
  animate={{
    scale: showOverlay ? 1.1 : 1,
    filter: showOverlay ? "blur(10px)" : "blur(0px)",
  }}
  transition={{ duration: 0.8 }}
>
  <motion.div
  initial={{ scale: 1.2, filter: "blur(15px)" }}
  animate={{
    scale: showOverlay ? 1.2 : 1,
    filter: showOverlay ? "blur(15px)" : "blur(0px)",
  }}
  transition={{ duration: 1 }}
>
  <MapView onMapClick={handleClick} />
</motion.div>
</motion.div>

      {/* 🔥 HERO OVERLAY */}
      {showOverlay && (
  <motion.div
    initial={{ opacity: 1 }}
    animate={{
      opacity: showOverlay ? 1 : 0,
      clipPath: showOverlay
        ? "circle(150% at 50% 50%)"
        : "circle(0% at 50% 50%)"
    }}
    transition={{ duration: 1, ease: "easeInOut" }}
    style={overlayStyle}
  >
    <motion.div
      initial={{ y: 40, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ delay: 0.3 }}
      style={{ textAlign: "center" }}
    >
      <h1 style={titleStyle}>🌍 EcoAir Insight</h1>

      <p style={{ opacity: 0.8, marginBottom: "20px" }}>
        AI-powered air quality intelligence across India
      </p>

      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => {
          setTimeout(() => setShowOverlay(false), 900);
        }}
        style={buttonStyle}
      >
        Explore Map →
      </motion.button>
    </motion.div>
  </motion.div>
)}

      {/* 🔄 LOADER */}
      {loading && <Loader />}

      {/* 📊 INFO PANEL */}
      {data && <InfoPanel data={data} />}
    </div>
  );
}

const overlayStyle = {
  position: "absolute",
  top: 0,
  left: 0,
  width: "100%",
  height: "100%",

  display: "flex",
  justifyContent: "center",
  alignItems: "center",

  // 🔥 NEW (NO DARK BOX)
  background: "linear-gradient(180deg, rgba(15,23,42,0.6), rgba(15,23,42,0.9))",
  backdropFilter: "blur(12px)",
  overflow : visible,
  zIndex: 999,
};

const titleStyle = {
  fontSize: "3rem",
  fontWeight: "bold",
  background: "linear-gradient(90deg, #38bdf8, #60a5fa)",
  WebkitBackgroundClip: "text",
  color: "transparent",
  marginBottom: "10px",

  // 🔥 FIXES CUTTING
  whiteSpace: "nowrap",
  overflow: "visible",
};

const buttonStyle = {
  padding: "12px 24px",
  background: "#38bdf8",
  border: "none",
  borderRadius: "8px",
  cursor: "pointer",
  fontSize: "1rem",
  color: "#0f172a",
  fontWeight: "bold",
};