export default function Navbar() {
  return (
    <div style={navStyle}>
      🌍 EcoAir Insight
    </div>
  );
}

const navStyle = {
  position: "absolute",
  top: 20,
  left: "50%",
  transform: "translateX(-50%)",
  padding: "10px 20px",
  borderRadius: "12px",

  background: "rgba(15,23,42,0.6)",
  backdropFilter: "blur(10px)",

  color: "#38bdf8",
  fontWeight: "bold",

  zIndex: 1000,
};