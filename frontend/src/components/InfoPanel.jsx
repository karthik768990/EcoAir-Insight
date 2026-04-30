import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import PredictionChart from "./PredictionChart";
import ReactMarkdown from "react-markdown";
import PollutantPanel from "./PollutantPanel";

export default function InfoPanel({ data, onClose }) {
  const [activeTab, setActiveTab] = useState("overview");

  if (!data) return null;
  const current = data.current || {};

  const getAQIColor = (aqi) => {
    if (!aqi) return "#94a3b8";
    if (aqi <= 50) return "#22c55e";
    if (aqi <= 100) return "#eab308";
    if (aqi <= 150) return "#f97316";
    if (aqi <= 200) return "#ef4444";
    if (aqi <= 300) return "#d946ef";
    return "#9f1239";
  };

  const aqiColor = getAQIColor(current?.aqi);

  const tabs = [
    { id: "overview", label: "Overview" },
    { id: "pollutants", label: "Pollutants" },
    { id: "ai", label: "AI Insights" },
    { id: "prediction", label: "Forecast" },
  ];

  return (
    <div style={containerStyle}>
      {/* 🛑 HEADER */}
      <div style={headerStyle}>
        <div>
          <h2 style={{ margin: 0, fontSize: "1.2rem", color: "#e2e8f0" }}>{data.station}</h2>
          <span style={{ fontSize: "0.8rem", color: "#94a3b8" }}>Station Data</span>
        </div>
        <button onClick={onClose} style={closeBtnStyle}>✕</button>
      </div>

      {/* 🟢 TABS NAVIGATION */}
      <div style={tabsContainerStyle}>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              ...tabBtnStyle,
              background: activeTab === tab.id ? "rgba(56, 189, 248, 0.15)" : "transparent",
              color: activeTab === tab.id ? "#38bdf8" : "#94a3b8",
              borderBottom: activeTab === tab.id ? "2px solid #38bdf8" : "2px solid transparent",
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* 🔵 CONTENT AREA */}
      <div style={contentStyle}>
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
          >
            {/* OVERVIEW TAB */}
            {activeTab === "overview" && (
              <div style={card}>
                <div style={{ textAlign: "center", marginBottom: "16px" }}>
                  <div style={{ fontSize: "3.5rem", fontWeight: "bold", color: aqiColor, lineHeight: "1" }}>
                    {current?.aqi ? Math.round(current.aqi) : "--"}
                  </div>
                  <div style={{ fontSize: "0.9rem", color: "#94a3b8", marginTop: "4px" }}>Air Quality Index</div>
                </div>

                <div style={{ background: "rgba(249, 115, 22, 0.1)", border: "1px solid rgba(249, 115, 22, 0.2)", padding: "12px", borderRadius: "8px", marginBottom: "16px" }}>
                  <h4 style={{ color: "#f97316", margin: "0 0 6px 0" }}>Health Advice</h4>
                  <p style={{ margin: 0, fontSize: "0.9rem", fontWeight: "600" }}>{data.health?.category}</p>
                  <p style={{ margin: "4px 0 0 0", fontSize: "0.85rem", opacity: 0.8 }}>{data.health?.advice}</p>
                </div>

                <div style={grid}>
                  <div style={statBox}>
                    <span style={label}>PM2.5</span>
                    <span style={value}>{current?.pm25 || "--"}</span>
                  </div>
                  <div style={statBox}>
                    <span style={label}>PM10</span>
                    <span style={value}>{current?.pm10 || "--"}</span>
                  </div>
                  <div style={statBox}>
                    <span style={label}>Temp</span>
                    <span style={value}>{current?.temp ? `${(current.temp).toFixed(2)}°C` : "--"}</span>
                  </div>
                  <div style={statBox}>
                    <span style={label}>Humidity</span>
                    <span style={value}>{current?.rh ? `${current.rh}%` : "--"}</span>
                  </div>
                </div>
              </div>
            )}

            {/* POLLUTANTS TAB */}
            {activeTab === "pollutants" && (
              <PollutantPanel data={current} />
            )}

            {/* AI INSIGHTS TAB */}
            {activeTab === "ai" && (
              <div style={card}>
                <h3 style={{ color: "#a78bfa", margin: "0 0 12px 0" }}>AI Analysis</h3>
                <div style={aiBox} className="markdown">
                  <ReactMarkdown>{data.ai_insights}</ReactMarkdown>
                </div>
              </div>
            )}

            {/* PREDICTION TAB */}
            {activeTab === "prediction" && (
              <div style={card}>
                <h3 style={{ color: "#22c55e", margin: "0 0 12px 0" }}>5-Year AQI Forecast</h3>
                {data.prediction?.length > 0 ? (
                  <PredictionChart data={data.prediction} />
                ) : (
                  <p style={{ opacity: 0.6 }}>No prediction data available for this station.</p>
                )}
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}

/* 🎨 STYLES */
const containerStyle = {
  display: "flex",
  flexDirection: "column",
  height: "100%",
  color: "#e2e8f0",
};

const headerStyle = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  padding: "16px",
  borderBottom: "1px solid rgba(255, 255, 255, 0.05)",
};

const closeBtnStyle = {
  background: "rgba(255,255,255,0.1)",
  border: "none",
  borderRadius: "50%",
  width: "30px",
  height: "30px",
  color: "#fff",
  cursor: "pointer",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  transition: "all 0.2s",
};

const tabsContainerStyle = {
  display: "flex",
  overflowX: "auto",
  padding: "0 8px",
  borderBottom: "1px solid rgba(255, 255, 255, 0.05)",
  scrollbarWidth: "none", // Firefox
  "&::-webkit-scrollbar": { display: "none" } // Note: won't work perfectly inline, but fine for now
};

const tabBtnStyle = {
  padding: "12px 16px",
  border: "none",
  cursor: "pointer",
  fontSize: "0.85rem",
  fontWeight: "600",
  transition: "all 0.2s",
  display: "flex",
  alignItems: "center",
  whiteSpace: "nowrap",
};

const contentStyle = {
  padding: "16px",
  overflowY: "auto",
  flex: 1,
};

const card = {
  background: "rgba(30, 41, 59, 0.6)",
  padding: "16px",
  borderRadius: "12px",
  border: "1px solid rgba(255, 255, 255, 0.05)",
};

const grid = {
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: "10px",
};

const statBox = {
  background: "rgba(15, 23, 42, 0.4)",
  padding: "10px",
  borderRadius: "8px",
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  border: "1px solid rgba(255, 255, 255, 0.03)",
};

const weatherRow = {
  display: "flex",
  justifyContent: "space-between",
  padding: "8px 0",
  borderBottom: "1px solid rgba(255, 255, 255, 0.05)",
  fontSize: "0.95rem",
};

const label = {
  fontSize: "0.8rem",
  color: "#94a3b8",
  marginBottom: "4px",
};

const value = {
  fontSize: "1.1rem",
  fontWeight: "bold",
  color: "#e2e8f0",
};

const aiBox = {
  background: "linear-gradient(135deg, rgba(168,85,247,0.1), rgba(59,130,246,0.05))",
  padding: "16px",
  borderRadius: "10px",
  border: "1px solid rgba(168,85,247,0.2)",
  fontSize: "0.9rem",
  lineHeight: "1.6",
};