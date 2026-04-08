import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import { useState } from "react";
import "leaflet/dist/leaflet.css";

function ClickHandler({ onClick, setPosition }) {
  useMapEvents({
    click(e) {
      setPosition(e.latlng);
      onClick(e.latlng);
    },
  });
  return null;
}

export default function MapView({ onMapClick }) {
  const [position, setPosition] = useState(null);

  return (
    <MapContainer
      center={[20.5937, 78.9629]}
      zoom={5}
      style={{ height: "100vh", width: "100%" }}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      <ClickHandler onClick={onMapClick} setPosition={setPosition} />

      {position && <Marker position={position} />}
    </MapContainer>
  );
}