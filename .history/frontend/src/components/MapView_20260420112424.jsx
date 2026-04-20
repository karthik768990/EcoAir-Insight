import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { useEffect } from "react";

// 🔥 Handles clicks + keeps map reference synced
function ClickHandler({ onClick, setMapRef }) {
  const map = useMapEvents({
    click(e) {
      // Zoom animation
      map.flyTo(e.latlng, 10, {
        duration: 1.5,
      });

      onClick(e.latlng);
    },
  });

  // 🔥 IMPORTANT: expose map instance to parent
  useEffect(() => {
    if (setMapRef) {
      setMapRef(map);
    }
  }, [map]);

  return null;
}

export default function MapView({ onMapClick, markerPosition, mapRef }) {
  return (
    <MapContainer
      center={[20.5937, 78.9629]}
      zoom={5}
      style={{ height: "100vh", width: "100%" }}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      <ClickHandler
        onClick={onMapClick}
        setMapRef={(mapInstance) => (mapRef.current = mapInstance)}
      />

      {/* 🔥 USE PARENT STATE (IMPORTANT) */}
      {markerPosition && <Marker position={markerPosition} />}
    </MapContainer>
  );
}