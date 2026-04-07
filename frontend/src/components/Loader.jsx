export default function Loader() {
  return (
    <div style={style}>
      <div className="spinner"></div>
    </div>
  );
}

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  zIndex: 1000
};