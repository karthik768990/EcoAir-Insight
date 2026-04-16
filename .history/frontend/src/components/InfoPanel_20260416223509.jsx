import { motion } from "framer-motion";
import PredictionChart from "./PredictionChart";
import ReactMarkdown from "react-markdown";

export default function InfoPanel({ data }) {
if (!data) return null;

const current = data.current || {};
const getAQIColor = (aqi) => {
  if (!aqi) return "#94a3b8";
  if (aqi <= 50) return "#22c55e";
  if (aqi <= 100) return "#eab308";
  if (aqi <= 150) return "#f97316";
  return "#ef4444";
};
return (
<motion.div
initial={{ x: 300, opacity: 0 }}
animate={{ x: 0, opacity: 1 }}
style={panelStyle}
>
{/* 🔥 HEADER */} <div style={header}>
  <h3 style={{ margin: 0 }}>{data.station}</h3>

  <div
    style={{
      fontSize: "2.2rem",
      fontWeight: "bold",
      color: getAQIColor(current?.aqi),
    }}
  >
    {Math.round(current?.aqi || 0)}
  </div>

  <span
    style={{
      fontSize: "0.75rem",
      background: getAQIColor(current?.aqi),
      padding: "3px 8px",
      borderRadius: "6px",
      color: "#0f172a",
      fontWeight: "bold",
    }}
  >
    AQI
  </span>
</div>

  {/* 🌫 POLLUTION CARD */}
<div style={card}>
  <h4>Pollution</h4>

  <div style={grid}>
    {current?.pm25 && <><span style={label}>PM2.5</span><span style={value}>{current.pm25}</span></>}
    {current?.pm10 && <><span style={label}>PM10</span><span style={value}>{current.pm10}</span></>}
    {current?.no2 && <><span style={label}>NO2</span><span style={value}>{current.no2}</span></>}
    {current?.so2 && <><span style={label}>SO2</span><span style={value}>{current.so2}</span></>}
  </div>
</div>
  {/* 🌦 WEATHER CARD */}
<div style={card}>
  <h4>Weather</h4>

  <div style={grid}>
    {current?.temp && <><span style={label}>Temp</span><span style={value}>{current.temp}°C</span></>}
    {current?.rh && <><span style={label}>Humidity</span><span style={value}>{current.rh}%</span></>}
    {current?.ws && <><span style={label}>Wind</span><span style={value}>{current.ws}</span></>}
  </div>
</div>
  {/* ⚠️ HEALTH */}
  <div style={card}>
    <h3>Health</h3>
    <p>{data.health?.category}</p>
    <p style={{ opacity: 0.7 }}>{data.health?.advice}</p>
  </div>

  {/* 🧠 AI INSIGHTS */}
  <div style={card}>
    <h3>AI Insights</h3>
    <div style={{ fontSize: "0.85rem", lineHeight: "1.5" }}>
      <ReactMarkdown>{data.ai_insights}</ReactMarkdown>
    </div>
  </div>

  {/* 📈 GRAPH */}
  {data.prediction?.length > 0 && (
    <div style={card}>
      <h3>Prediction</h3>
      <PredictionChart data={data.prediction} />
    </div>
  )}
</motion.div>

);
}

/* 🎨 STYLES */
const panelStyle = {
  position: "relative",
  top: 20,
  right: 20,
  width: "300px",
  maxHeight: "85vh",
  overflowY: "auto",
  padding: "14px",
  borderRadius: "14px",

  background: "rgba(15, 23, 42, 0.75)", // lighter
  backdropFilter: "blur(8px)",

  boxShadow: "0 10px 30px rgba(0,0,0,0.4)",
  zIndex: 1000,
};

const card = {
  background: "rgba(30, 41, 59, 0.6)",
  padding: "12px",
  borderRadius: "12px",
  marginBottom: "12px",
  border: "1px solid rgba(148, 163, 184, 0.1)",
};
const grid = {
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: "6px",
  fontSize: "0.9rem",
};

const label = {
  opacity: 0.6,
};

const value = {
  textAlign: "right",
  fontWeight: "500",
};