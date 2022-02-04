export default function zoomToSearchGeometries(map, group) {
    map.eachLayer((layer) => {
      if (layer.feature?.properties.source === 'search') {
        group.addLayer(layer)
      }
    })
  
    if (Object.keys(group._layers).length > 0) {
      map.fitBounds(group.getBounds())
    }
  }
