/**
 * Updates the paths in the content object based on the provided array of paths.
 *
 * @param {Object} content - The content object containing paths to be updated.
 * @param {Object[]} paths - The array of paths to update the content with.
 * @param {string} paths[].terrain - The terrain type of the path.
 * @param {number} paths[].lat - The latitude of the marker on the path.
 * @param {number} paths[].lng - The longitude of the marker on the path.
 *
 * @returns {Object} - The updated content object with paths.
 * @property {number} length - The total number of paths after the update.
 * @property {Object[]} paths - The updated array of paths.
 * @property {string} paths[].terrain - The terrain type of the path.
 * @property {Object[]} paths[].markers - The array of markers on the path.
 * @property {number} paths[].markers[].lat - The latitude of the marker on the path.
 * @property {number} paths[].markers[].lng - The longitude of the marker on the path.
 */
export function updatePaths(content, paths) {
  let currentState = content.length ? content.paths.pop() : null;
  let pathsToAppend = [];
  for (let i = content.length; i < paths.length; i++) {
    const marker = paths[i];

    // If there has not been any content, set the current state to the first
    // marker and continue.
    if (!currentState) {
      currentState = {
        terrain: marker.terrain,
        markers: [{ lat: marker.lat, lng: marker.lng }],
      };
    }

    // If the marker's terrain is the same as the current state's terrain,
    // append the marker to the current state's markers.
    else if (currentState.terrain === marker.terrain) {
      currentState.markers.push({ lat: marker.lat, lng: marker.lng });
    }

    // If the marker's terrain is different than the current state's terrain,
    // append the current state to the content and set the current state to the
    // marker.
    else {
      pathsToAppend.push(currentState);
      currentState = {
        terrain: marker.terrain,
        markers: [
          // Add previous marker to the current set of markers to maintain a continuous path
          currentState.markers[currentState.markers.length - 1], 
          { lat: marker.lat, lng: marker.lng },
        ],
      };
    }
  }
  if (currentState) {
    pathsToAppend.push(currentState);
  }
  return {
    length: paths.length,
    paths: [...content.paths, ...pathsToAppend],
  };
}

export function generateColor(terrain) {
    switch(terrain) {
        case "grass":
            return "#00ff00";
        case "asphalt":
            return "#000000";
        default:
            return "#ffffff";
    }
}
