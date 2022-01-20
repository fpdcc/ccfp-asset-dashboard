import ReactDOM from 'react-dom'
import React, { useState, useEffect } from 'react'
import { GeoJSON } from 'react-leaflet'
import hash from 'object-hash'
import Cookies from 'js-cookie'
import BaseMap from './BaseMap'
import AreaClipper from '../map_utils/AreaClipper'
import AssetSearchTable from '../tables/AssetSearchTable'

function AssetTypeOptions() {
  // these options could come from the server but hardcoding for now 
  const options = [
    {value: 'buildings', label: 'Buildings'},
    {value: 'trails', label: 'Trails'}
  ]

  return options.map(option => {
    return <option value={option.value} key={option.value}>{option.label}</option>
  })
}

function AssetsMap(props) {
  const [searchedGeoms, setSearchedGeoms] = useState()
  const [existingGeoms, setExistingGeoms] = useState()
  const [clippedGeoms, setClippedGeoms] = useState(null)
  const [searchText, setSearchText] = useState('')
  const [searchedAssetType, setSearchedAssetType] = useState('buildings')

  useEffect(() => {
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

  function searchAssets() {
    const url = `/assets/?` + new URLSearchParams({
      'q': searchText,
      'asset_type': searchedAssetType
    })

    fetch(url, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFTOKEN': Cookies.get('csrftoken')
      },
      mode: 'same-origin',
      method: 'GET'
    }).then((response) => response.json())
    .then((data) => setSearchedGeoms(data))
    .catch(error => {
      // TODO: show an error message in the UI
      console.log('error', error)
    })
  }
 
  return (
    <div className='row'>
      <div className='col-4'>
        <div className='row'>
          <div className='input-group'>
            <label htmlFor='asset-search' className='sr-only'>Search for Assets</label>
            <input 
              type='search'
              onChange={(e) => setSearchText(e.target.value)}
              value={searchText}
              className='form-control' 
              aria-label='Search for assets' 
              placeholder='Search for assets' />
            <select
              className='form-control'
              value={searchedAssetType}
              onChange={(e) => setSearchedAssetType(e.target.value)}
            >
              <AssetTypeOptions />
            </select>
            <button 
              onClick={() => searchAssets()}
              className='btn btn-warning'>
                Search
            </button>
          </div>
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
            <button 
              className='btn btn-primary'
              onClick={() => saveGeometries()}>
              Save Asset
            </button>
          </div>
          : 
          <div className='col-10'>
            <p>Use the map toolbar to select an asset.</p>
          </div>
        }
        <div className='map-viewer' aria-label='Asset Selection Map'>
          <BaseMap
            center={[41.8781, -87.6298]}
            zoom={11}
            whenCreated={onMapCreated}>
            <AreaClipper 
              geoJson={searchedGeoms}
              onClipped={onClipped} />
            {searchedGeoms && 
              <>
                <GeoJSON 
                  data={searchedGeoms} 
                  // Hash key tells the geojson to re-render 
                  // when the state changes: https://stackoverflow.com/a/46593710
                  key={hash(searchedGeoms)} 
                  style={{color: 'black'}}
                />
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
  React.createElement(AssetsMap, window.props),
  window.reactMount
)
