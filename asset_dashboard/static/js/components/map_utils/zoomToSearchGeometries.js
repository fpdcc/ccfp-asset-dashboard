export default function zoomToSearchGeometries(map, group) {
    map.eachLayer((layer) => {
      if (layer.feature?.properties.identifier) {
        // If "identifier" is in "properties",
        // then this is a feature from the search.
        // This is extremely dependent on the search geometries
        // having this "identifier" key, so beware!
        // I haven't been able to figure out a better
        // way of zooming in on the search results.
        group.addLayer(layer)
      }
    })
  
    if (Object.keys(group._layers).length > 0) {
      map.fitBounds(group.getBounds())
    }
  }
