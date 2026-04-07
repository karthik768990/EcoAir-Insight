import { motion } from "framer-motion";
import PredictionChart from "./PredictionChart";
import ReactMarkdown from "react-markdown";

const markdownStyle = {
  fontSize: "0.9rem",
  lineHeight: "1.5",
};


const sectionTitle = {
  marginTop: "15px",
  color: "#38bdf8",
  borderBottom: "1px solid #334155",
  paddingBottom: "5px",
};

export default function InfoPanel({ data }) {
  if(!data)return null;  
  return (
    <motion.div
      initial={{ x: 300, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      style={panel(data?.health?.color || "#3b82f6")}
>
      <h2>{data.station}</h2>
<h3 style={sectionTitle}>Air Quality</h3>
<p>AQI: {data.current?.aqi}</p>

<h3 style={sectionTitle}>Pollutants</h3>
<p>PM2.5: {data.current?.pm25}</p>
<p>PM10: {data.current?.pm10}</p>

<h3 style={sectionTitle}>Health</h3>
<p>{data.health?.category}</p>
<p>{data.health?.advice}</p>

<h3 style={sectionTitle}>AI Insights</h3>
<div className="markdown" style={markdownStyle}>
  <ReactMarkdown>{data.ai_insights}</ReactMarkdown>
</div>
      {data.prediction.length > 0 && (
        <PredictionChart data={data.prediction} />
      )}
    </motion.div>
  );
}

const panel = (color) => ({
  position: "absolute",
  top: 20,
  right: 20,
  width: "360px",
  maxHeight: "90vh",   // 🔥 important
  overflowY: "auto",   // 🔥 scroll
  padding: "20px",
  background: "rgba(30, 41, 59, 0.95)",
  backdropFilter: "blur(10px)",
  borderRadius: "16px",
  borderLeft: `6px solid ${color}`,
  boxShadow: "0 0 30px rgba(0,0,0,0.5)",
  zIndex: 1000
});