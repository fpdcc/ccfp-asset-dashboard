import React, { useEffect } from 'react'
import { useMap } from 'react-leaflet'
import zoomToSearchGeometries from './zoomToSearchGeometries'


function MapZoom({ searchGeoms }) { 
  const map = useMap()

  useEffect(() => {
    const group = new L.featureGroup()
    zoomToSearchGeometries(map, group)
  }, [searchGeoms])

  return null
}

export default MapZoom
