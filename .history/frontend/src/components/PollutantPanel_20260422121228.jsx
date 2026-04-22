import React from "react";

const getStatusColor = (status) => {
  if (status === "Safe") return "#22c55e";
  if (status === "Moderate") return "#facc15";
  if (status === "High") return "#ef4444";
  return "#94a3b8";
};

export default function PollutantPanel({ data }) {
  if (!data || !data.pollutants) return null;

  const pollutants = data.pollutants;
  const major = data.major_pollutant;
  const explanation = data.explanation;

  return (
    <div style={card}>
      <h3 style={title}>🌫 Pollutant Analysis</h3>

      {/* 🔥 LIST */}
      {Object.values(pollutants).map((p, i) => (
        <div key={i} style={row}>
          <span>{p.name}</span>

          <span>{p.value} µg/m³</span>

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

      {/* 🔥 MAJOR */}
      {major && (
        <div style={majorBox}>
          🔥 {major.name} is dominant
        </div>
      )}

      {/* 🔥 EXPLANATION */}
      {explanation && (
        <p style={explain}>{explanation}</p>
      )}
    </div>
  );
}

const card = {
  background: "#1e293b",
  padding: "12px",
  borderRadius: "10px",
  marginBottom: "10px",
};

const title = {
  color: "#38bdf8",
  marginBottom: "8px",
};

const row = {
  display: "flex",
  justifyContent: "space-between",
  marginBottom: "6px",
};

const badge = {
  padding: "2px 8px",
  borderRadius: "8px",
  color: "#0f172a",
  fontSize: "0.75rem",
  fontWeight: "600",
};

const majorBox = {
  marginTop: "10px",
  padding: "8px",
  background: "rgba(239,68,68,0.2)",
  borderRadius: "6px",
};

const explain = {
  marginTop: "6px",
  fontSize: "0.85rem",
  color: "#cbd5f5",
};