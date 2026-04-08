export default function Particles() {
  return (
    <div style={style}>
      {[...Array(30)].map((_, i) => (
        <div key={i} style={particle(i)} />
      ))}
    </div>
  );
}

const style = {
  position: "absolute",
  width: "100%",
  height: "100%",
  top: 0,
  left: 0,
  pointerEvents: "none",
  zIndex: 1,
};

const particle = (i) => ({
  position: "absolute",
  width: "4px",
  height: "4px",
  borderRadius: "50%",
  background: "#38bdf8",
  opacity: 0.6,

  top: Math.random() * 100 + "%",
  left: Math.random() * 100 + "%",

  animation: `float ${5 + Math.random() * 5}s infinite ease-in-out`,
}); 