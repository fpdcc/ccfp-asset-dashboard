import React, { useEffect, useState } from 'react'
import { FeatureGroup } from 'react-leaflet'
import clip from 'turf-clip'
import EditControl from './EditControl'

export default function MapClipper({ geoJson, onClipped }) {
  const [drawnGeometries, setDrawnGeometries] = useState(null)

  useEffect(() => {
    clipGeometries(drawnGeometries)
  }, [drawnGeometries])

  function onEdited(e) {
    let editedLayers = {}

    for (const [key, layer] of Object.entries(e.layers._layers)) {
      const geoJSON = layer.toGeoJSON()

      editedLayers = {
        ...editedLayers,
        [key]: geoJSON
      }
    }

    setDrawnGeometries(prevState => {
      return {
        ...prevState,
        ...editedLayers
      }
    })
  }

  function onCreated(e) {
    const geoJSON = e.layer.toGeoJSON()

    setDrawnGeometries(prevState => {
      return {
        ...prevState,
        [e.layer._leaflet_id]: geoJSON
      }
    })
  }

  function onDeleted(e) {
    setDrawnGeometries(prevState => {
      for (const [key, layer] of Object.entries(e.layers._layers)) {
        delete prevState[key]
      }
      return {
        ...prevState
      }
    })
  }

  function clipGeometries(geometries) {
    if (geometries) {
      const bounds = {
        'type': 'FeatureCollection',
        'features': Object.values(geometries)
      }
  
      const clippedFeatureCollection = clip(bounds, geoJson)
  
      if (clippedFeatureCollection.features.length > 0) {
        onClipped(clippedFeatureCollection)
      }
    } else {
      // geometries aren't truthy, which means they were deleted
      // or the component mounted the first time. In either case,
      // send back null so that the caller has no clipped geoms.
      onClipped(null)
    }
  }
  
  return (
    <FeatureGroup>
      <EditControl 
        onEdited={onEdited}
        onCreated={onCreated}
        onDeleted={onDeleted}
        position='topright'
        draw={{
          polygon: {
            allowIntersection: false
          },
          rectangle: {
            allowIntersection: false
          },
          circle: false,
          marker: false,
          polyline: false,
          circlemarker: false,
        }}
      />
    </FeatureGroup>
  )
}
