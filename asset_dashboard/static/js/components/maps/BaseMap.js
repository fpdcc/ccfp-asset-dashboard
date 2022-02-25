import React from 'react'
import { MapContainer, TileLayer } from 'react-leaflet'

function BaseMap({ center, zoom, className, whenCreated, children }) {
  return (
    <MapContainer
      center={center} 
      zoom={zoom}
      className={className}
      whenCreated={whenCreated}
      >
      <TileLayer
        url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright" target="_parent">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions" target="_parent">CARTO</a>'
      />
      {children} 
  </MapContainer>
  )
}

export default BaseMap