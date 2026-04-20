import { useState } from "react";

export default function LatLonSearch({ onSearch }) {
  const [lat, setLat] = useState("");
  const [lon, setLon] = useState("");

  const handleSearch = () => {
    const latNum = parseFloat(lat);
    const lonNum = parseFloat(lon);

    if (isNaN(latNum) || isNaN(lonNum)) {
      alert("Enter valid numbers");
      return;
    }

    onSearch(latNum, lonNum);
  };

  return (
    <div style={container}>
      <input
        type="text"
        placeholder="Lat"
        value={lat}
        onChange={(e) => setLat(e.target.value)}
        style={input}
      />

      <input
        type="text"
        placeholder="Lon"
        value={lon}
        onChange={(e) => setLon(e.target.value)}
        style={input}
      />

      <button onClick={handleSearch} style={button}>
        Go
      </button>
    </div>
  );
}

const container = {
  position: "absolute",
  bottom: "20px",
  left: "20px",
  zIndex: 1000,
  background: "rgba(15,23,42,0.9)",
  padding: "10px",
  borderRadius: "10px",
  display: "flex",
  gap: "6px",
};

const input = {
  width: "90px",
  padding: "6px",
  borderRadius: "6px",
  border: "1px solid #334155",
  background: "#1e293b",
  color: "#e2e8f0",
};

const button = {
  padding: "6px 10px",
  borderRadius: "6px",
  background: "#22c55e",
  border: "none",
  fontWeight: "bold",
  cursor: "pointer",
};