export default function zoomToExistingGeometries(map, group) {
  map.eachLayer((layer) => {
    if (layer.feature) {
      group.addLayer(layer)
    }
  })
  
  if (Object.keys(group._layers).length > 0) {
    map.fitBounds(group.getBounds())
  }
}
