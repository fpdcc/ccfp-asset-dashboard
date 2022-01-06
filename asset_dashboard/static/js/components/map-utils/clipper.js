import React, { useState, useRef } from 'react'
import { useMap } from 'react-leaflet'
import clip from 'turf-clip'
import { polygon } from '@turf/turf'
import { debounce } from 'lodash'

// This component controls the interaction for selecting a part, whole, or group of
// assets. A user can select an area by holding shift and dragging a box
// over the map with their mouse. This clips the intersection of the bounding box
// and any geojson assets within the box. The component doesn't return anything in the UI, 
// but has side effects via a callback that sends the clipped FeatureCollection to 
// the parent component.

export default function AreaClipper({ geoJson, onClipped }) {
  const [selectedArea, setSelectedArea] = useState(null)

  const map = useMap()

  function clipArea(e, selectedArea, setSelectedArea, onClipped) {
    const northEast = e.boxZoomBounds._northEast
    const southWest = e.boxZoomBounds._southWest

    const northEastLatLng = [northEast.lat, northEast.lng]
    const southWestLatLng = [southWest.lat, southWest.lng]

    // Clean up previous selectedArea rectangle
    if (selectedArea) {
      map.removeLayer(selectedArea)
    }

    // Create the new bounds
    const bounds = L.latLngBounds([northEastLatLng, southWestLatLng])

    // Update the map to show the bounds
    const rectangle = L.rectangle(bounds, { color: 'orange', opacity: 0.2 })

    rectangle.addTo(map)

    // Add it to state so we can remove it later
    setSelectedArea(rectangle)

    // Format the bounds to (long, lat) so the polygon 
    // matches the incoming geojson SRID.
    const boundsPoly = polygon([
      [
        [bounds.getNorthEast().lng, bounds.getNorthEast().lat],
        [bounds.getNorthWest().lng, bounds.getNorthWest().lat],
        [bounds.getSouthWest().lng, bounds.getSouthWest().lat],
        [bounds.getSouthEast().lng, bounds.getSouthEast().lat],
        [bounds.getNorthEast().lng, bounds.getNorthEast().lat],
      ],
    ])

    // TODO: test what happens when the geojson is a line (like a trail)
    const clippedFeatureCollection = clip(boundsPoly, geoJson)

    if (clippedFeatureCollection.features.length > 0) {
      onClipped(clippedFeatureCollection)
    }
  }

  // Prevent the clipArea function from firing multiple times.
  // See:
  // 1) https://stackoverflow.com/q/37081698/
  // 2) https://stackoverflow.com/a/28610565
  // 3) https://newbedev.com/lodash-debounce-not-working-in-react
  const clipAreaDebounced = useRef(debounce(clipArea), 100)

  map.on('boxzoomend', (e) => {
    clipAreaDebounced.current(e, selectedArea, setSelectedArea, onClipped)
  })

  return null
}
