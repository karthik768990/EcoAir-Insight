import React from "react";

const getStatusColor = (status) => {
  if (status === "Safe") return "#22c55e";
  if (status === "Moderate") return "#facc15";
  if (status === "High") return "#ef4444";
  return "#94a3b8";
};

export default function PollutantPanel({ data }) {
  if (!data || !data.pollutants) {
  return (
    <div style={card}>
      <h3 style={title}>🌫 Pollutant Analysis</h3>
      <p style={{ opacity: 0.6 }}>No pollutant data available</p>
    </div>
  );
}

  const pollutants = data.pollutants || {};
  const major = data.major_pollutant;
  const explanation = data.explanation;

  return (
    <div style={card}>
      <h3 style={title}>🌫 Pollutant Analysis</h3>

      {/* 🔥 Pollutant List */}
      <div style={list}>
        {Object.values(pollutants).map((p, index) => (
          <div key={index} style={row}>
            <span style={label}>{p.name}</span>

            <span style={value}>
              {p.value} µg/m³
            </span>

            <span
              style={{
                ...badge,
                background: getStatusColor(p.status),
              }}
            >
              {p.status}
            </span>
          </div>
        ))}
      </div>

      {/* 🔥 Major Pollutant */}
      {major && (
        <div style={majorBox}>
          <strong>🔥 Major Pollutant: {major.name}</strong>
          <div style={{ fontSize: "0.8rem", opacity: 0.8 }}>
            Ratio: {major.ratio}
          </div>
        </div>
      )}

      {/* 🔥 Explanation */}
      {explanation && (
        <p style={explain}>
          {explanation}
        </p>
      )}
    </div>
  );
}

const card = {
  background: "rgba(30, 41, 59, 0.7)",
  padding: "12px",
  borderRadius: "12px",
  marginBottom: "12px",
  border: "1px solid rgba(148, 163, 184, 0.1)",
};

const title = {
  marginBottom: "8px",
  color: "#38bdf8",
};

const list = {
  display: "flex",
  flexDirection: "column",
  gap: "6px",
};

const row = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  fontSize: "0.9rem",
};

const label = {
  opacity: 0.7,
};

const value = {
  fontWeight: "500",
};

const badge = {
  padding: "2px 8px",
  borderRadius: "10px",
  fontSize: "0.75rem",
  color: "#0f172a",
  fontWeight: "600",
};

const majorBox = {
  marginTop: "10px",
  padding: "8px",
  borderRadius: "8px",
  background: "rgba(239, 68, 68, 0.15)",
  border: "1px solid rgba(239, 68, 68, 0.3)",
};

const explain = {
  marginTop: "8px",
  fontSize: "0.85rem",
  color: "#cbd5f5",
};