import { useState } from "react";
import axios from "axios";
import MapView from "../components/MapView";
import InfoPanel from "../components/InfoPanel";

export default function MapPage() {
  const [data, setData] = useState(null);

  const handleClick = async (latlng) => {
    const res = await axios.get(
      `http://localhost:8000/analysis?lat=${latlng.lat}&lon=${latlng.lng}`
    );
    setData(res.data);
  };

  return (
    <div>
      <MapView onMapClick={handleClick} />
      {data && <InfoPanel data={data} />}
    </div>
  );
}