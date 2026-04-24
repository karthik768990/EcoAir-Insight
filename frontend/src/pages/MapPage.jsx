import { useState, useRef } from "react";
import axios from "axios";
import { motion } from "framer-motion";

import LatLonSearch from "../components/LatLonSearch";
import MapView from "../components/MapView";
import InfoPanel from "../components/InfoPanel";
import Loader from "../components/Loader";
import Particles from "../components/Particles";
import Navbar from "../components/Navbar";

export default function MapPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showOverlay, setShowOverlay] = useState(true);
  const [markerPosition, setMarkerPosition] = useState(null);
  const [mapTheme, setMapTheme] = useState("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png");

  const mapRef = useRef();

  const BASE_URL = import.meta.env.VITE_BACKEND_URL;

  const MAP_THEMES = [
    { name: "Dark", url: "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" },
    { name: "Light", url: "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png" },
    { name: "Street", url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" },
    { name: "Satellite", url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}" }
  ];

  // 🔥 MAP CLICK HANDLER
  const handleClick = async (latlng) => {
    setLoading(true);
    setData(null);

    try {
      const res = await axios.get(
        `${BASE_URL}/analysis?lat=${latlng.lat}&lon=${latlng.lng}`
      );

      setData(res.data);
      setMarkerPosition([latlng.lat, latlng.lng]);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  // 🔥 LAT-LON SEARCH HANDLER
const handleLatLonSearch = (lat, lon) => {
  // 🔥 simulate map click
  handleClick({
    lat,
    lng: lon
  });

  // 🔥 move map (smooth animation)
  if (mapRef.current) {
    mapRef.current.flyTo([lat, lon], 10, {
      duration: 1.5
    });
  }
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
            width: "100%",
            height: "100%",
            position: "relative"
          }}
        >
          <MapView
            onMapClick={handleClick}
            markerPosition={markerPosition}
            mapRef={mapRef}
            themeUrl={mapTheme}
          />

          {/* 🔥 MAP THEME SWITCHER */}
          <div style={themeSwitcherStyle}>
            {MAP_THEMES.map((theme) => (
              <button
                key={theme.name}
                onClick={() => setMapTheme(theme.url)}
                style={{
                  ...themeBtnStyle,
                  background: mapTheme === theme.url ? "#38bdf8" : "rgba(15, 23, 42, 0.8)",
                  color: mapTheme === theme.url ? "#0f172a" : "#e2e8f0",
                }}
              >
                {theme.name}
              </button>
            ))}
          </div>

          {/* 🔥 LAT LON SEARCH (BOTTOM LEFT) */}
          <LatLonSearch onSearch={handleLatLonSearch} />
        </motion.div>

        {/* 📊 FLOATING PANEL */}
        {data && (
          <motion.div
            initial={{ x: 400, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: 400, opacity: 0 }}
            style={{
              position: "absolute",
              top: "80px", // Below navbar
              right: "20px",
              width: "380px",
              maxHeight: "calc(100vh - 100px)",
              background: "rgba(15, 23, 42, 0.65)",
              backdropFilter: "blur(16px)",
              borderRadius: "16px",
              border: "1px solid rgba(255,255,255,0.1)",
              boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.5)",
              overflowY: "auto",
              zIndex: 1000,
              padding: "0" // Padding handled inside InfoPanel now
            }}
          >
            <InfoPanel data={data} onClose={() => setData(null)} />
          </motion.div>
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
            <h1 style={titleStyle}>EcoAir Insight</h1>

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

const themeSwitcherStyle = {
  position: "absolute",
  top: "80px",
  left: "20px",
  zIndex: 1000,
  display: "flex",
  flexDirection: "column",
  gap: "6px",
  background: "rgba(15, 23, 42, 0.5)",
  backdropFilter: "blur(10px)",
  padding: "8px",
  borderRadius: "12px",
  border: "1px solid rgba(255, 255, 255, 0.1)",
};

const themeBtnStyle = {
  padding: "6px 12px",
  border: "none",
  borderRadius: "6px",
  cursor: "pointer",
  fontSize: "0.85rem",
  fontWeight: "600",
  transition: "all 0.2s ease",
  textAlign: "left",
};