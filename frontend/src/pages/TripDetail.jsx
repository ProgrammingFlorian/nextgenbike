import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import GoogleMapReact from "google-map-react";

import Marker from "../components/map/Marker";
import Polyline from "../components/map/Polyline";

import { API_URL, dummyMarkers, additionalMarkers } from "../constants";

import { updatePaths } from "../utils";

import axios from "axios";

export default function TripDetail() {
  const { id } = useParams();

  const [mapsLoaded, setMapsLoaded] = useState(false);
  const [map, setMap] = useState(null);
  const [maps, setMaps] = useState(null);

  const defaultPath = {
    length: 0,
    paths: [],
  };

  const [markers, setMarkers] = useState([{
    lat: 40.7128,
    lng: -74.006,
  }]);
  const [paths, setPaths] = useState(defaultPath);

  // const markers = [
  //   { lat: 53.42728, lng: -6.24357 },
  //   { lat: 43.681583, lng: -79.61146 },
  // ];

  const defaultProps = {
    center: {
      lat: 40.7128,
      lng: -74.006,
    },
    zoom: 11,
  };

  const apiIsLoaded = (map, maps) => {
    setMapsLoaded(true);
    setMap(map);
    setMaps(maps);

    fitBounds(map, maps);
  };

  function fitBounds(map, maps) {
    var bounds = new maps.LatLngBounds();
    for (let marker of markers) {
      bounds.extend(new maps.LatLng(marker.lat, marker.lng));
    }
    map.fitBounds(bounds);
  }

  // function fitBounds(map, maps, markers) {
  //   var bounds = new maps.LatLngBounds();
  //   for (let marker of markers) {
  //     bounds.extend(new maps.LatLng(marker.lat, marker.lng));
  //   }
  //   map.fitBounds(bounds);
  // }

  function afterMapLoadChanges() {
    return (
      <div style={{ display: "none" }}>
        {paths.paths.map((path, index) => {
          return (
            <Polyline
              key={index}
              map={map}
              maps={maps}
              markers={path.markers}
              color={path.terrain === "grass" ? "#00FF00" : "#000000"}
            />
          );
        })}
        {/* <Polyline map={map} maps={maps} markers={markers} /> */}
      </div>
    );
  }

  useEffect(() => {
    // setMarkers(dummyMarkers);
    // setPaths(updatePaths(defaultPath, dummyMarkers));
    // dummyMarkers.push(...additionalMarkers);
    const intervalId = setInterval(() => {
      // This code will be executed every second
      axios.get(`${API_URL}/terrain`).then((response) => {
        const markers = response.data;
        console.log(markers);
        setMarkers(markers);
        setPaths(updatePaths(paths, markers));
        // fitBounds(map, maps);
        // afterMapLoadChanges();
      });
    }, 5000);
      // axios.get(`${API_URL}/terrain`).then((response) => {
      //   const markers = response.data;
      //   console.log(markers);
      //   setMarkers(markers);
      //   setPaths(updatePaths(paths, markers));
      // });

    // This function will be called when the component unmounts
    return () => {
      // Clear the interval to avoid memory leaks
      clearInterval(intervalId);
    };
  }, []);

  return (
    <div className="">
      {/* Welcome Message */}
      <div className="p-9 mt-4">
        <div className="flex flex-col gap-0.5">
          <h1 className="text-2xl font-bold">Trip Detail</h1>
        </div>
      </div>
      {/* Render Map */}
      {console.log(paths)}
      <div
        className="absolute bottom-18 z-0 "
        style={{ height: "76vh", width: "100%" }}
      >
        <GoogleMapReact
          key={markers.length}  // Add a key attribute here
          bootstrapURLKeys={{ key: import.meta.env.VITE_MAPS_API_KEY }}
          defaultCenter={defaultProps.center}
          defaultZoom={defaultProps.zoom}
          yesIWantToUseGoogleMapApiInternals
          onGoogleApiLoaded={({ map, maps }) => apiIsLoaded(map, maps)}
        >
          <Marker text="A" lat={40.7128} lng={-74.006} />
          {console.log(paths)}
          {/* <Marker text={'YYZ'} lat={43.681583} lng={-79.61146} /> */}
          {mapsLoaded ? afterMapLoadChanges() : ""}
        </GoogleMapReact>
      </div>
    </div>
  );
}
