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
{/* 🔥 HEADER */} <div style={header}> <h2>{data.station}</h2>
<h1 style={{ fontSize: "2.5rem", margin: 0 }}>
{current?.aqi || "--"} </h1>
<p style={{ opacity: 0.7 }}>Air Quality Index</p> </div>

```
  {/* 🌫 POLLUTION CARD */}
  <div style={card}>
    <h3>Pollution</h3>
    <div style={grid}>
      <span>PM2.5</span><span>{current?.pm25}</span>
      <span>PM10</span><span>{current?.pm10}</span>
      <span>NO2</span><span>{current?.no2}</span>
      <span>SO2</span><span>{current?.so2}</span>
      <span>CO</span><span>{current?.co}</span>
      <span>Ozone</span><span>{current?.ozone}</span>
    </div>
  </div>

  {/* 🌦 WEATHER CARD */}
  <div style={card}>
    <h3>Weather</h3>
    <div style={grid}>
      <span>Temp</span><span>{current?.temp} °C</span>
      <span>Humidity</span><span>{current?.rh}%</span>
      <span>Wind</span><span>{current?.ws} m/s</span>
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
width: "340px",
maxHeight: "90vh",
overflowY: "auto",
padding: "16px",
borderRadius: "16px",
background: "rgba(15, 23, 42, 0.9)",
backdropFilter: "blur(10px)",
boxShadow: "0 0 30px rgba(0,0,0,0.5)",
zIndex: 1000,
};

const header = {
marginBottom: "15px",
textAlign: "center",
};

const card = {
background: "rgba(30, 41, 59, 0.8)",
padding: "12px",
borderRadius: "12px",
marginBottom: "12px",
};

const grid = {
display: "grid",
gridTemplateColumns: "1fr 1fr",
gap: "6px",
fontSize: "0.9rem",
};
