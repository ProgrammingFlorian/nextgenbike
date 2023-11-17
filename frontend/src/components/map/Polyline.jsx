export default function Polyline({ color, markers, map, maps }) {
    let geodesicPolyline = new maps.Polyline({
        path: markers,
        geodesic: true,
        strokeColor: color,
        strokeOpacity: 1.0,
        strokeWeight: 6
    })
    geodesicPolyline.setMap(map)
    return null;
}
