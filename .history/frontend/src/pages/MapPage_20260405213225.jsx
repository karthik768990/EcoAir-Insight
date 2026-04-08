import { useState } from "react";
import axios from "axios";
import MapView from "../components/MapView";
import InfoPanel from "../components/InfoPanel";
import Loader from "../components/Loader";

export default function MapPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const BASE_URL = import.meta.env.VITE_BACKEND_URL;

  const handleClick = async (latlng) => {
    setLoading(true);
    setData(null);

    try {
      const res = await axios.get(
        `${BASE_URL}/analysis?lat=${latlng.lat}&lon=${latlng.lng}`
      );
      console.log("API DATA:", res.data);

      setData(res.data);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };
  return (
  <div style={{ position: "relative" }}>
    <MapView onMapClick={handleClick} />

    {loading && <Loader />}
    {data && <InfoPanel data={data} />}
  </div>
);
}