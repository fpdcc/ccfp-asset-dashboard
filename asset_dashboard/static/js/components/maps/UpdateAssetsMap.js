import ReactDOM from 'react-dom'
import React, { useState, useEffect } from 'react'
import { GeoJSON, useMap } from 'react-leaflet'
import Select from 'react-select'
import hash from 'object-hash'
import Cookies from 'js-cookie'


import BaseMap from './base'
import AreaClipper from '../map-utils/clipper'
import AssetSearchTable from '../tables/AssetSearchTable'
import SearchInput from '../SearchInput'

function MapZoom() {
  const map = useMap()

  const group = new L.featureGroup()
  map.eachLayer((layer) => {
    console.log('map each layer')
    console.log(layer)
    if (layer.feature) {
      console.log('if layer feature')
      group.addLayer(layer)
    }
  })

    

    if (Object.keys(group._layers).length > 0) {
      map.fitBounds(group.getBounds())
    }
  return null
}

function UpdateAssetsMap(props) {
  const [searchedGeoms, setSearchedGeoms] = useState()
  const [existingGeoms, setExistingGeoms] = useState()
  const [clippedGeoms, setClippedGeoms] = useState(null)
  const [searchText, setSearchText] = useState('')
  const [searchedAssetType, setSearchedAssetType] = useState({value: 'buildings', label: 'Buildings'})
  // const map = useMap()

  useEffect(() => {
    if (props?.existing_geoms) {
      setExistingGeoms(JSON.parse(props.existing_geoms))
    }
  }, [setSearchedGeoms, setExistingGeoms])

  function onMapCreated(map) {
    const group = new L.featureGroup()

    map.eachLayer((layer) => {
      console.log('map each layer')
      console.log(layer)
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

  function onSuccessfulSearch(data) {
    setSearchedGeoms(data)

    onMapCreated(map)
  }

  function searchAssets() {
    const url = `/assets/?` + new URLSearchParams({
      'q': searchText,
      'asset_type': searchedAssetType.value
    })

    fetch(url, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFTOKEN': Cookies.get('csrftoken'),
        'credentials': 'same-origin'
      },
      method: 'GET'
    }).then((response) => response.json())
    .then((data) => onSuccessfulSearch(data))
    .catch(error => {
      console.log('error', error)
    })
  }
 
  return (
    <div className='row'>
      <div className='col-4'>
        <div className='row'>
          <SearchInput 
            className='d-flex justify-content-between px-2 col-12'
            onFilter={(e) => setSearchText(e.target.value)}
            filterText={searchText}
            placeholder='Search for assets'
            ariaLabel='Search for assets'
          />
          <Select 
            className='col'
            id='select-asset-type'
            // we could programatically get this from the backend but hardcoding for now
            options={[
              {value: 'buildings', label: 'Buildings'},
              {value: 'trails', label: 'Trails'}
            ]}
            value={searchedAssetType}
            onChange={(value) => setSearchedAssetType(value)}
          />
          <button 
            onClick={() => searchAssets()}
            className='btn btn-secondary'>
            Search
          </button>
        </div>
        {searchedGeoms && 
          <AssetSearchTable
            rows={searchedGeoms.features}
          />
        }
      </div>
      <div className='col'>
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
            <p>Use the map toolbar to select an asset.</p>
          </div>
        }
        <div className='map-viewer' aria-label='Asset Selection Map'>
          <BaseMap
            center={[41.8781, -87.6298]}
            zoom={11}
            whenCreated={onMapCreated}>
              {/* {searchedGeoms && <MapZoom />} */}
            {/* <AreaClipper 
              geoJson={searchedGeoms}
              onClipped={onClipped} /> */}
            {/* TODO: what colors do we want to use? do we need a legend? */}
            {searchedGeoms && 
              <>
                <GeoJSON 
                data={searchedGeoms} 
                // Hash key tells the geojson to re-render 
                // when the state changes: https://stackoverflow.com/a/46593710
                key={hash(searchedGeoms)} 
                style={{color: 'black'}}
                />
                <MapZoom />
              </>
                }
            {existingGeoms && <GeoJSON data={existingGeoms} style={{color: 'green'}}/>}
          </BaseMap>
        </div>
      </div>
    </div>
  )
}

ReactDOM.render(
  React.createElement(UpdateAssetsMap, window.props),
  window.reactMount
)
