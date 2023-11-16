import { useParams } from "react-router-dom";
import GoogleMapReact from "google-map-react";

export default function TripDetail() {
  const { id } = useParams();
  const defaultProps = {
    center: {
      lat: 59.95,
      lng: 30.33,
    },
    zoom: 11,
  };
  return (
    <div className="">
      {/* Welcome Message */}
      <div className="p-9 mt-4">
        <div className="flex flex-col gap-0.5">
          <h1 className="text-2xl font-bold">Trip Detail</h1>
        </div>
      </div>
      {/* Render Map */}
      {console.log(import.meta.env.VITE_MAPS_API_KEY)}
      <div
        className="absolute bottom-18 z-0 "
        style={{ height: "76vh", width: "100%" }}
      >
        <GoogleMapReact
          bootstrapURLKeys={{ key: import.meta.env.VITE_MAPS_API_KEY }}
          defaultCenter={defaultProps.center}
          defaultZoom={defaultProps.zoom}
        ></GoogleMapReact>
      </div>
    </div>
  );
}
