import PredictionChart from "./PredictionChart";

export default function InfoPanel({ data }) {
  return (
    <div style={panel(data.health.color)}>
      <h2>{data.station}</h2>

      <div style={row}>
        <span>AQI</span>
        <strong>{data.current.aqi}</strong>
      </div>

      <div style={row}>
        <span>PM2.5</span>
        <strong>{data.current.pm25}</strong>
      </div>

      <div style={row}>
        <span>PM10</span>
        <strong>{data.current.pm10}</strong>
      </div>

      <hr />

      <h3>{data.health.category}</h3>
      <p>{data.health.advice}</p>

      <hr />

      <h4>AI Insights</h4>
      <p style={{ fontSize: "0.9rem" }}>{data.ai_insights}</p>

      {/* 🔥 GRAPH */}
      {data.prediction.length > 0 && (
        <>
          <h4>Prediction</h4>
          <PredictionChart data={data.prediction} />
        </>
      )}
    </div>
  );
}

const panel = (color) => ({
  position: "absolute",
  top: 20,
  right: 20,
  width: "320px",
  padding: "20px",
  background: "#1e293b",
  borderRadius: "12px",
  borderLeft: `6px solid ${color}`,
  boxShadow: "0 0 20px rgba(0,0,0,0.4)",
});

const row = {
  display: "flex",
  justifyContent: "space-between",
};