import { useState, useEffect } from "react";
import axios from "axios";
import { API_URL } from "../constants";

export default function Homepage() {
  const [keyword, setKeyword] = useState("");
  const [trips, setTrips] = useState([]);

  useEffect(() => {
    axios.get(`${API_URL}/trips`).then((res) => {
      setTrips(res.data);
    });
  }, []);

  return (
    <div className="p-9 mt-4">
      {/* Welcome Message */}
      <div className="flex flex-col gap-0.5">
        <h1 className="text-2xl font-bold">Your Recent Trips</h1>
      </div>

      {/* Search Bar */}
      <input
        className="text-sm py-2 px-4 mt-8 border border-gray w-full rounded-lg"
        type="text"
        value={keyword}
        placeholder="Search Trip ..."
        onChange={(e) => setKeyword(e.target.value)}
      />

      {/* Render Small Items */}
      {trips.map((trip, index) => (
        <div key={index}>
          {trip.name}
        </div>
      ))}
    </div>
  );
}
