import React, { useEffect } from 'react'
import { useMap } from 'react-leaflet'

export default function ShowPopup({ geojson }) {
  const map = useMap()

  useEffect(() => {
    map.eachLayer((layer) => {
      if (layer.feature == geojson) {
        console.log('layer.feature == geojson')
        console.log('layer.feature', layer.feature)
        console.log('geojson', geojson)
        layer.openPopup()

        // Make the layer appear selected.
        if (layer.setStyle) {
          layer.setStyle({
            fillColor: '#3388ff',
            fillOpacity: '0.2',
            color: '#3388ff',
            weight: '4'
          })
        }
      }
    })
  }, [geojson])

  return null
}
