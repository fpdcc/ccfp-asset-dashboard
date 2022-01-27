import React, { useEffect, useState } from 'react'
import { FeatureGroup } from 'react-leaflet'
import clip from 'turf-clip'
import EditControl from './EditControl'

export default function MapClipper({ geoJson, onClipped }) {
  console.log('i render')
  // TODO: rename this to drawnGeometries or something like it
  const [selectedGeometries, setSelectedGeometries] = useState(null)
  const [deletedGeometries, setDeletedGeometries] = useState(null)

  useEffect(() => {
    console.log('useEffect', selectedGeometries)
    if (selectedGeometries) {
      clipGeometries(selectedGeometries)
    }

    if (deletedGeometries) {
      
    }
  }, [clipGeometries])

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

    const newGeometries = {
      ...selectedGeometries,
      ...editedLayers
    }

    // setSelectedGeometries(newGeometries)

    clipGeometries(newGeometries)
  }

  function onCreated(e) {
    const geoJSON = e.layer.toGeoJSON()

    setSelectedGeometries(prevState => {
      return {
        ...prevState,
        [e.layer._leaflet_id]: geoJSON
      }
    })

    // const newGeometries = {
    //   ...selectedGeometries,
    //   [e.layer._leaflet_id]: geoJSON
    // }

    // console.log('onCreated', newGeometries)

    // // clipGeometries(newGeometries)
    // setSelectedGeometries(newGeometries)
    // clipGeometries()
    
  }

  function onDeleted(e) {
    const layersKeys = getLayersKeys(e.layers._layers)
    console.log('layersKeys', layersKeys)
    console.log('selectedGeometries', selectedGeometries)

    // let newGeometries = selectedGeometries

    // console.log('newGeometries', newGeometries)
    // layersKeys.forEach(key => {
    //   delete newGeometries[key]
    // })

    // if (newGeometries) {
    //   clipGeometries(newGeometries)
    // }
  }

  function getLayersKeys(layers) {
    return Object.keys(layers).map(key => { return key })
  }

  function clipGeometries(geoms) {
    console.log('clipGeometries', geoms)
    const bounds = {
      'type': 'FeatureCollection',
      'features': Object.values(geoms)
    }

    const clippedFeatureCollection = clip(bounds, geoJson)

    if (clippedFeatureCollection.features.length > 0) {
      onClipped(clippedFeatureCollection)
    }

    setSelectedGeometries(geoms)
  }

  console.log('selectedGeometries', selectedGeometries)
  
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
