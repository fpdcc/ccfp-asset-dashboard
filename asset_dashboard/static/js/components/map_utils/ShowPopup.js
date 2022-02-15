import React, { useEffect } from 'react'
import { useMap } from 'react-leaflet'
import bindPopup from '../map_utils/bindPopup'

export default function ShowPopup({ geojson }) {
  const map = useMap()

  useEffect(() => {
    map.eachLayer((layer) => {
      if (layer.feature == geojson) {
        layer.openPopup()
      }
    })
  }, [geojson])

  return null
}
