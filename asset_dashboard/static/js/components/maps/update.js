import ReactDOM from 'react-dom'
import React, { useState, useEffect } from 'react'
import { GeoJSON } from 'react-leaflet'
import BaseMap from '../maps/base'
import AreaClipper from '../map-utils/clipper'
import UpdateForm from '../maps/update-form'
import Cookies from 'js-cookie'

function UpdateMap(props) {
  const [searchedGeoms, setSearchedGeoms] = useState()
  const [existingGeoms, setExistingGeoms] = useState()
  const [clippedGeoms, setClippedGeoms] = useState(null)

  useEffect(() => {
    if (props?.search_geoms) {
      setSearchedGeoms(JSON.parse(props.search_geoms))
    }

    // TODO: implement this on the backend
    if (props?.existing_geoms) {
      setExistingGeoms(JSON.parse(props.existing_geoms))
    }
  }, [setSearchedGeoms, setExistingGeoms])

  function onMapCreated(map) {
    const group = new L.featureGroup()

    map.eachLayer((layer) => {
      if (layer.feature) {
        group.addLayer(layer)
      }
    })

    if (Object.keys(group._layers).length > 0) {
      map.fitBounds(group.getBounds())
    }
  }

  function onClipped(featureCollection) {
    console.log(JSON.stringify(featureCollection))
    setClippedGeoms(featureCollection)
  }

  console.log(document.cookie)

  function saveGeometries() {
    console.log('save them')
    console.log(clippedGeoms)

    fetch(window.location.pathname, {
        headers: {
            'Cookie': document.cookie,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': Cookies.get('csrftoken')
        },
        method: 'POST',
        body: JSON.stringify(clippedGeoms)
    }).then((response) => {
      if (response.status == 301) {
        setClippedGeoms(null)
      }
    })
}

  return (
    <div>
      {clippedGeoms && 
        <div>
          <select>
            {/* TODO: select so they can associate with a phase...is this neccessary? */}
            {/* Do we need to associate an asset with a phase? How does this work when
                an asset will inevitably get added to every phase? */}
          </select>
          <button onClick={() => saveGeometries()}>
            Save Asset
          </button>
        </div>
      }
      <div className='map-viewer' aria-label='Asset Selection Map'>
        <BaseMap
          center={[41.8781, -87.6298]}
          zoom={11}
          whenCreated={onMapCreated}
        >
          <AreaClipper 
            geoJson={searchedGeoms}
            onClipped={onClipped} />
          {/* TODO: what colors do we want to use? do we need a legend? */}
          <GeoJSON data={searchedGeoms} style={{color: 'green'}}/> 
          <GeoJSON data={existingGeoms} style={{color: 'dark-green', opacity: 0.8}}/>
        </BaseMap>
      </div>
    </div>
  )
}

ReactDOM.render(
  React.createElement(UpdateMap, window.props),
  window.reactMount
)
