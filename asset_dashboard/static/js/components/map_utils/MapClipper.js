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
    const layerKeys = getLayersKeys(e.layers._layers)

    let editedLayers = {}

    layerKeys.forEach(layerKey => {
      const layer = e.layers._layers[layerKey]

      const geoJSON = layer.toGeoJSON()

      editedLayers = {
        ...editedLayers,
        [layerKey]: geoJSON
      }
    })

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
    const layersKeys = getLayersKeys(e.layers._layers)

    setDrawnGeometries(prevState => {
      layersKeys.forEach(key => {
        delete prevState[key]
      })
      return {
        ...prevState
      }
    })
  }

  function getLayersKeys(layers) {
    return Object.keys(layers).map(key => { return key })
  }

  function clipGeometries(geometries) {
    if (geometries) {
      const bounds = {
        'type': 'FeatureCollection',
        'features': Object.values(geometries)
      }
  
      const clippedFeatureCollection = clip(bounds, geoJson)
      console.log('clippedFeatureCollection', clippedFeatureCollection)
  
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

  console.log('selectedGeometries', drawnGeometries)
  
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
