import React, { useEffect } from 'react'
import { useMap } from 'react-leaflet'

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
