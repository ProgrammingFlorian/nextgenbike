import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import GoogleMapReact from "google-map-react";

import Marker from "../components/map/Marker";
import Polyline from "../components/map/Polyline";

import { API_URL, dummyMarkers, additionalMarkers } from "../constants";

import { updatePaths } from "../utils";

import axios from "axios";

import { generateColor } from "../utils";

const terrainLegend = [
  {
    terrain: 0,
    label: "Asphalt",
  },
  {
    terrain: 1,
    label: "Pavement",
  },
  {
    terrain: 2,
    label: "Gravel",
  },
  {
    terrain: 3,
    label: "Grass",
  },
];
export default function TripDetail() {
  const { id } = useParams();

  const [mapsLoaded, setMapsLoaded] = useState(false);
  const [map, setMap] = useState(null);
  const [maps, setMaps] = useState(null);

  const defaultPath = {
    length: 0,
    paths: [],
  };

  const [markers, setMarkers] = useState([
    {
      lat: 1.2944905,
      lng: 103.7746889,
    },
  ]);
  const [paths, setPaths] = useState(defaultPath);

  // const markers = [
  //   { lat: 53.42728, lng: -6.24357 },
  //   { lat: 43.681583, lng: -79.61146 },
  // ];

  const defaultProps = {
    center: {
      lat: 1.2944905,
      lng: 103.7746889,
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
              color={generateColor(path.terrain)}
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
      axios
        .post(
          `${API_URL}/terrain`,
          {
            trip_id: parseInt(id),
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        )
        .then((response) => {
          const markers = response.data;
          console.log(markers);
          setMarkers(
            markers.map((marker) => ({
              lat: marker.latitude,
              lng: marker.longitude,
            }))
          );
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
      <div className="absolute w-full z-10 bottom-28">
        <div className="flex justify-left ml-6">
          <div className="bg-white p-4 w-4/5 border border-gray border-opacity-50 flex flex-col text-left rounded-lg">
            <span className="font-bold">Legend</span>
            <div className="grid grid-cols-2">
              {terrainLegend.map((item, idx) => (
                <div key={idx} className="flex flex-row gap-2">
                  <span
                    style={{
                      backgroundColor: generateColor(item.terrain),
                      padding: "4px",
                      marginTop: "auto",
                      marginBottom: "auto",
                    }}
                  />
                  <span>{item.label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
      {/* Render Map */}
      {console.log(paths)}
      <div
        className="absolute bottom-18 z-0 "
        style={{ height: "76vh", width: "100%" }}
      >
        <GoogleMapReact
          key={markers.length}
          bootstrapURLKeys={{ key: import.meta.env.VITE_MAPS_API_KEY }}
          defaultCenter={defaultProps.center}
          defaultZoom={defaultProps.zoom}
          yesIWantToUseGoogleMapApiInternals
          onGoogleApiLoaded={({ map, maps }) => apiIsLoaded(map, maps)}
        >
          {console.log(paths)}
          {/* <Marker text={'YYZ'} lat={43.681583} lng={-79.61146} /> */}
          {mapsLoaded ? afterMapLoadChanges() : ""}
        </GoogleMapReact>
      </div>
    </div>
  );
}
