import ReactDOM from 'react-dom'
import React, { useEffect } from 'react'
import BaseMap from './BaseMap'
import { GeoJSON } from 'react-leaflet'
import zoomToExistingGeometries from '../map_utils/zoomToExistingGeometries'
import circleMarker from '../map_utils/circleMarker'
import ReactTable from '../BaseTable'
import existingAssetsColumns from '../table_utils/existingAssetsColumns'
import bindPopup from '../map_utils/bindPopup'

function ListAssetsMap(props) {

  const onMapCreated = (map) => {
    const group = new L.featureGroup()
    zoomToExistingGeometries(map, group)
  }

  return (
    <>
      {
        props?.assets && 
          <div className='border border-secondary rounded'>
            <div className='row'>
              <div className='col-4 m-3'>
                <div className="d-flex align-items-center justify-content-between m-2">
                  <h3>Phase Assets</h3>
                  <a href={`${window.location.href}assets`} class="btn btn-warning ml-4">Edit Assets ></a>
                </div>
                <div className='map-thumbnail'>
                  <BaseMap
                    center={[41.8781, -87.6298]}
                    zoom={11}
                    whenCreated={onMapCreated}>
                    <GeoJSON 
                      data={props.assets} 
                      style={{color: 'green'}} 
                      pointToLayer={circleMarker}
                      onEachFeature={bindPopup}
                    />
                  </BaseMap>
                </div>
              </div>
              <div className='col m-3'>
                <ReactTable 
                  rows={props.assets.features}
                  columns={React.useMemo(() =>  existingAssetsColumns(), [])}
                  pageSizeIncrements={[10]}
                  sizeOfPage={10}
                />
              </div>
            </div>
          </div>
      }
    </>
  )
}

ReactDOM.render(
  React.createElement(ListAssetsMap, window.props),
  window.reactMount
)
