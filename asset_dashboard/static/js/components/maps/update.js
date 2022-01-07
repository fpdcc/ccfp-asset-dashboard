import ReactDOM from 'react-dom'
import React, { useState, useEffect } from 'react'
import { GeoJSON } from 'react-leaflet'
import BaseMap from '../maps/base'
import AreaClipper from '../map-utils/clipper'
import Cookies from 'js-cookie'
import Select from 'react-select'

function UpdateMap(props) {
  const [searchedGeoms, setSearchedGeoms] = useState()
  const [existingGeoms, setExistingGeoms] = useState()
  const [clippedGeoms, setClippedGeoms] = useState(null)
  const [phases, setPhases] = useState(null)
  const [selectedPhase, setSelectedPhase] = useState(null)

  useEffect(() => {
    if (props?.search_geoms) {
      setSearchedGeoms(JSON.parse(props.search_geoms))
    }

    if (props?.existing_geoms) {
      setExistingGeoms(JSON.parse(props.existing_geoms))
    }

    const phaseOptions = makePhaseOptions(props.phases)
    setPhases(phaseOptions)
    setSelectedPhase(phaseOptions[0])
  }, [setSearchedGeoms, setExistingGeoms, setPhases])

  function makePhaseOptions(inputPhases) {
    return inputPhases.map(phase => {
      return {
        value: phase.id.toString(),
        label: `${phase.estimated_bid_quarter} - ${phase.phase_type} - ${phase.status}`
      }
    })
  }

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
     // TODO: implement the ability to click on a single asset? 
     // Or does having only one way to select make for a better UX?
    setClippedGeoms(featureCollection)
  }

  function saveGeometries() {
    fetch(window.location.pathname, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': Cookies.get('csrftoken')
        },
        method: 'POST',
        mode: 'same-origin',
        body: JSON.stringify({
          'geojson': clippedGeoms,
          'phase': selectedPhase.value
        })
    }).then((response) => {
      if (response.status == 200) {
        location.reload()
        // TODO: show success message
        // https://stackoverflow.com/questions/13256817/django-how-to-show-messages-under-ajax-function
      } else {
        // TODO: catch error and show message
      }
    })
  }
 
  return (
    <div>
      {clippedGeoms 
        ?
        <div className='row'>
          {/* This Select component is only for a proof of concept. We can tweak this however we need.
           Not the best UI right now (that Z-index under the map!).*/}
          {/* Do we need to associate an asset with a phase? How does this work when
              an asset will inevitably get added to every phase? */}
          <Select 
            id='phases'
            className='col-8'
            value={selectedPhase}
            options={phases}
            onChange={(value) => setSelectedPhase(value)}
            menuPosition='fixed' 
            menuPortalTarget={document.body} />
          <button 
            className='btn btn-primary'
            onClick={() => saveGeometries()}>
            Save Asset
          </button>
        </div>
        : 
        <div className='col-10'>
          {/* // TODO: better languge!!! */}
          <p>Select part of an asset, an entire asset, or a group of assets by holding shift and dragging a box over the assets.</p>
        </div>
      }
      <div className='map-viewer mt-5' aria-label='Asset Selection Map'>
        <BaseMap
          center={[41.8781, -87.6298]}
          zoom={11}
          whenCreated={onMapCreated}>
          <AreaClipper 
            geoJson={searchedGeoms}
            onClipped={onClipped} />
          {/* TODO: what colors do we want to use? do we need a legend? */}
          <GeoJSON data={searchedGeoms} style={{color: 'black'}}/>
          {existingGeoms && <GeoJSON data={existingGeoms} style={{color: 'green'}}/>}
        </BaseMap>
      </div>
    </div>
  )
}

ReactDOM.render(
  React.createElement(UpdateMap, window.props),
  window.reactMount
)
