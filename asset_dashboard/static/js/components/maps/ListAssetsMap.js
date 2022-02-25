import ReactDOM from 'react-dom'
import React, { useEffect } from 'react'
import BaseMap from './BaseMap'
import { GeoJSON } from 'react-leaflet'
import zoomToExistingGeometries from '../map_utils/zoomToExistingGeometries'
import circleMarker from '../map_utils/circleMarker'

function ListAssetsMap(props) {

  const onMapCreated = (map) => {
    const group = new L.featureGroup()
    zoomToExistingGeometries(map, group)
  }

  return (
    <div className='map-container'>
      <BaseMap
      center={[41.8781, -87.6298]}
      zoom={11}
      whenCreated={onMapCreated}>
        {
          props?.assets && 
            <GeoJSON 
              data={props.assets} 
              style={{color: 'green'}} 
              pointToLayer={circleMarker}
            />
        }
      </BaseMap>
    </div>
  )
}

ReactDOM.render(
  React.createElement(ListAssetsMap, window.props),
  window.reactMount
)
