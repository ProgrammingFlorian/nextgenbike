import { useState, useEffect } from "react";
import axios from "axios";
import { API_URL } from "../constants";
import { useNavigate } from "react-router-dom";

export default function Homepage() {
  const [keyword, setKeyword] = useState("");
  const [trips, setTrips] = useState([]);
  
  const navigate = useNavigate();

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

      <div className="flex flex-col gap-2 mt-4 mb-20">
        {/* Render Small Items */}
        {trips.map((trip, index) => {
          const startDate = new Date(trip.start);
          const endDate = new Date(trip.end);
          return (
            <div
              key={index}
              className="p-3 border border-gray rounded-lg border-opacity-50"
              onClick={() => navigate(`/trips/${trip.id}`)}
            >
              <div className="grid grid-cols-12 text-center">
                <span>📌</span>
                <span>{trip.id}</span>
                <span className="col-span-10 text-left ml-2">{trip.name}</span>
                <span className="col-span-2"></span>
                <span className="col-span-10 text-left ml-2 text-gray text-sm">
                  {startDate.toLocaleDateString()} -{" "}
                  {endDate.toLocaleDateString()}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
