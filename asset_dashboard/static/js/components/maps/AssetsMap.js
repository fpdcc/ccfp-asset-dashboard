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
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    if (props?.existing_assets) {
      setExistingGeoms(props.existing_assets)
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
    const data = clippedGeoms['features'].map(feature => {
      return {
        'asset_id': feature['properties']['identifier'],
        'asset_type': searchedAssetType,
        'asset_name': feature['properties']['name'],
        'geom': feature['geometry']
      }
    })

    fetch('/local-assets/', {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': Cookies.get('csrftoken')
        },
        method: 'POST',
        mode: 'same-origin',
        body: JSON.stringify(data)
    }).then((response) => {
      if (response.status == 201) {
        // TODO: this reloads the page but clears the user search...
        // Need to come up with way to reload by rehydrating the previous state
        location.reload()
        // TODO: show success message
        // https://stackoverflow.com/questions/13256817/django-how-to-show-messages-under-ajax-function
      }
    }).catch(error => {
      // TODO show error message
      console.error(error)
    })
  }

  function searchAssets() {
    setIsLoading(true)

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
    .then((data) => {
      setIsLoading(false)
      setSearchedGeoms(data)
    })
    .catch(error => {
      // TODO: show an error message in the UI
      console.error('error', error)
    })
  }
 
  return (
    <div className='row'>
      <div className='col-4'>
        <div className='row'>
          <div className='col'>
            <div className='row m-1'>
              <label htmlFor='asset-search' className='sr-only'>Search for Assets</label>
              <input 
                type='search'
                onChange={(e) => setSearchText(e.target.value)}
                value={searchText}
                className='form-control' 
                aria-label='Search for assets' 
                placeholder='Search for assets' />
            </div>
            <div className='row m-1'>
              <select
                className='form-control col mr-1'
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
        </div>
        <div>
          {isLoading ? 'Loading...' : null}
          {searchedGeoms && 
            <AssetSearchTable
              rows={searchedGeoms.features}
            />
          }
        </div>
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
            {searchedGeoms && 
              <>
                <GeoJSON 
                  data={searchedGeoms} 
                  // Hash key tells the geojson to re-render 
                  // when the state changes: https://stackoverflow.com/a/46593710
                  key={hash(searchedGeoms)} 
                  style={{color: 'black'}}
                />
                <AreaClipper 
                  geoJson={searchedGeoms}
                  onClipped={onClipped} />
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
