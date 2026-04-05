import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div style={styles.container}>
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        🌍 EcoAir Insight
      </motion.h1>

      <p>AI-powered air quality intelligence across India</p>

      <motion.button
        whileHover={{ scale: 1.1 }}
        onClick={() => navigate("/map")}
        style={styles.button}
      >
        Explore Map →
      </motion.button>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
  },
  button: {
    marginTop: "20px",
    padding: "12px 24px",
    background: "#2563eb",
    border: "none",
    color: "white",
    borderRadius: "8px",
    cursor: "pointer",
  },
};