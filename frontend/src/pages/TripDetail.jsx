import { useParams } from "react-router-dom";
import GoogleMapReact from "google-map-react";

export default function TripDetail() {
  const { id } = useParams();
  const defaultProps = {
    center: {
      lat: 40.7128,
      lng: -74.006,
    },
    zoom: 11,
  };
  const apiIsLoaded = (map, maps) => {
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);
    const origin = { lat: 1.298432, lng: 103.7756263 };
    const destination = { lat: 1.297204, lng: 103.778772 };

    directionsService.route(
      {
        origin: origin,
        destination: destination,
        travelMode: google.maps.TravelMode.DRIVING,
      },
      (result, status) => {
        if (status === google.maps.DirectionsStatus.OK) {
          directionsRenderer.setDirections(result);
        } else {
          console.error(`error fetching directions ${result}`);
        }
      }
    );
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
          yesIWantToUseGoogleMapApiInternals
          onGoogleApiLoaded={({ map, maps }) => apiIsLoaded(map, maps)}
        ></GoogleMapReact>
      </div>
    </div>
  );
}
