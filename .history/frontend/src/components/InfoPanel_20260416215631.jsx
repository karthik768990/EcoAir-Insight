import { motion } from "framer-motion";
import PredictionChart from "./PredictionChart";
import ReactMarkdown from "react-markdown";

export default function InfoPanel({ data }) {
if (!data) return null;

const current = data.current || {};

return (
<motion.div
initial={{ x: 300, opacity: 0 }}
animate={{ x: 0, opacity: 1 }}
style={panelStyle}
>
{/* 🔥 HEADER */} <div style={{ textAlign: "center", marginBottom: "10px" }}>
  <h3 style={{ margin: 0 }}>{data.station}</h3>

  <div style={{
    fontSize: "2rem",
    fontWeight: "bold",
    marginTop: "5px"
  }}>
    {Math.round(current?.aqi || 0)}
  </div>

  <p style={{ opacity: 0.6, fontSize: "0.8rem" }}>
    AQI
  </p>
</div>

  {/* 🌫 POLLUTION CARD */}
<div style={card}>
  <h4>Pollution</h4>

  <div style={grid}>
    {current?.pm25 && <><span>PM2.5</span><span>{current.pm25}</span></>}
    {current?.pm10 && <><span>PM10</span><span>{current.pm10}</span></>}
    {current?.no2 && <><span>NO2</span><span>{current.no2}</span></>}
    {current?.so2 && <><span>SO2</span><span>{current.so2}</span></>}
  </div>
</div>
  {/* 🌦 WEATHER CARD */}
<div style={card}>
  <h4>Weather</h4>

  <div style={grid}>
    {current?.temp && <><span>Temp</span><span>{current.temp}°C</span></>}
    {current?.rh && <><span>Humidity</span><span>{current.rh}%</span></>}
    {current?.ws && <><span>Wind</span><span>{current.ws}</span></>}
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
  position: "absolute",
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