import React, { useEffect, useState } from 'react'
import { FeatureGroup } from 'react-leaflet'
import clip from 'turf-clip'
import * as turf from '@turf/turf'
import EditControl from './EditControl'

export default function MapClipper({ geoJson, onClipped }) {
  const [drawnGeometries, setDrawnGeometries] = useState(null)

  useEffect(() => {
    if (drawnGeometries) {
      clipGeometries(drawnGeometries)
    }
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

  /* Separate the geometry types. We need the LineStrings to clip, 
    and separately all of the other geometry types to see if they 
    intersect with the drawnGeometries. 
    A LineString would be a trail that can be clipped.
    The remaining types would be like a building or structure, etc
    that should be treated as an entire entity and not clipped. */
  function separateGeometryTypes() {
    const lineStringFeatureTypes = []
    const allOtherFeatureTypes = []
    
    turf.featureEach(geoJson, (currentFeature) => {
      if (['LineString', 'MultiLineString'].includes(turf.getType(currentFeature))) {
        lineStringFeatureTypes.push(currentFeature)
      } else {
        allOtherFeatureTypes.push(currentFeature)
      }
    })

    return [
      turf.featureCollection(lineStringFeatureTypes),
      turf.featureCollection(allOtherFeatureTypes)
    ]
  }

  function getIntersectingFeatures(bounds, featureCollection) {
    if (featureCollection) {
      const intersectingFeatures = []

      turf.featureEach(featureCollection, (currentFeature) => {
        if (turf.booleanIntersects(currentFeature, bounds)) {
          intersectingFeatures.push(currentFeature)
        }
      })

      return intersectingFeatures
    }

    return []
  }

  function getClippedFeatures(bounds, featureCollection) {
    if (featureCollection) {
      return clip(bounds, featureCollection).features
    }

    return []
  }

  function clipGeometries(geometries) {
    const [lineStringFeatureCollection, allOtherTypesFeatureCollection] = separateGeometryTypes()

    const bounds = turf.featureCollection(Object.values(geometries))

    const intersectingFeatures = getIntersectingFeatures(bounds, allOtherTypesFeatureCollection)

    const clippedFeatures = getClippedFeatures(bounds, lineStringFeatureCollection)

    const finalFeatureCollection = turf.featureCollection(intersectingFeatures.concat(clippedFeatures))

    if (finalFeatureCollection.features.length > 0) {
      onClipped(finalFeatureCollection)
    } else {
      // No features exist, which means they were deleted.
      // Send back null so that the caller has no clipped geometries.
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
