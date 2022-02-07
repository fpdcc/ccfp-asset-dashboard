import ReactDOM from 'react-dom'
import ReactDOMServer from 'react-dom/server'
import React, { useState, useEffect } from 'react'
import { GeoJSON } from 'react-leaflet'
import hash from 'object-hash'
import Cookies from 'js-cookie'
import { useSessionstorageState } from 'rooks'
import BaseMap from './BaseMap'
import AssetSearchTable from '../tables/AssetSearchTable'
import ExistingAssetsTable from '../tables/ExistingAssetsTable'
import MapClipper from '../map_utils/MapClipper'
import MapZoom from '../map_utils/MapZoom'
import zoomToSearchGeometries from '../map_utils/zoomToSearchGeometries'
import zoomToExistingGeometries from '../map_utils/zoomToExistingGeometries'
import Message from '../helpers/Message'
import Popup from '../map_utils/Popup'

function AssetTypeOptions() {
  // these options could come from the server but hardcoding for now 
  const options = [
    {value: 'buildings', label: 'Buildings'},
    {value: 'trails', label: 'Trails'},
    {value: 'points_of_interest', label: 'Points of Interest'}
  ]

  return options.map(option => {
    return <option value={option.value} key={option.value}>{option.label}</option>
  })
}

function SelectAssetsMap(props) {
  const [searchGeoms, setSearchGeoms] = useSessionstorageState('searchGeoms', null)
  const [existingGeoms, setExistingGeoms] = useState()
  const [clippedGeoms, setClippedGeoms] = useState(null)
  const [searchText, setSearchText] = useSessionstorageState('searchText', '')
  const [searchAssetType, setSearchAssetType] = useSessionstorageState('searchAssetTypes', 'buildings')
  const [isLoading, setIsLoading] = useState(false)
  const [phaseId, setPhaseId] = useState(null)
  const [ajaxMessage, setAjaxMessage] = useSessionstorageState('ajaxMessage', null)

  useEffect(() => {
    if (props?.existing_assets) {
      setExistingGeoms(props.existing_assets)
    }

    if (props?.phase_id) {
      setPhaseId(props.phase_id)
    }
  }, [])

  function onMapCreated(map) {
    const group = new L.featureGroup()

    if (searchGeoms) {
      zoomToSearchGeometries(map, group)
    } else {
      zoomToExistingGeometries(map, group)
    }
  }

  function onClipped(featureCollection) {
    setClippedGeoms(featureCollection)
  }

  function saveGeometries() {
    const data = clippedGeoms['features'].map(feature => {
      return {
        'asset_id': feature['properties']['identifier'],
        'asset_type': searchAssetType,
        'asset_name': feature['properties']['name'],
        'geom': feature['geometry'],
        'phase': phaseId
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
        setAjaxMessage({text: 'Assets successfully saved.', tag: 'success'})
        location.reload()
      }
    }).catch(error => {
      setAjaxMessage({text: 'An error occurred saving the selected assets. Please try again.', tag: 'danger'})
      console.error(error)
    })
  }

  function searchAssets() {
    setIsLoading(true)

    const url = `/assets/?` + new URLSearchParams({
      'q': searchText,
      'asset_type': searchAssetType
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
      setSearchGeoms(data)
    })
    .catch(error => {
      setIsLoading(false)
      setAjaxMessage({text: 'An error occurred searching for selected assets. Please try again.', tag: 'danger'})
      console.error('error', error)
    })
  }

  function pointToLayer(feature, latlng) {
    return L.circleMarker(
      latlng,
      {
        radius: 7,
        fillColor: 'green',
        weight: 1,
        opacity: 1,
        fillOpacity: 1
      }
    )
  }

  function onEachFeature(feature, layer) {
    const popupContent = ReactDOMServer.renderToString(
      <Popup feature={feature} />
    )

    layer.bindPopup(popupContent)
  }
 
  return (
    <>
      {ajaxMessage 
        ? <Message 
            text={ajaxMessage.text} 
            messageTag={ajaxMessage.tag} 
            onCloseMessage={setAjaxMessage}
          /> 
        : null
      }
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
                  value={searchAssetType}
                  onChange={(e) => setSearchAssetType(e.target.value)}
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
            {searchGeoms && 
              <AssetSearchTable
                rows={searchGeoms.features}
              />
            }
          </div>
        </div>
        <div className='col'>
          <div className='d-flex justify-content-end m-2'>
            {clippedGeoms 
              ?
                <button 
                  className='btn btn-primary'
                  onClick={() => saveGeometries()}>
                  Save Assets
                </button>
              : <p>Use the map toolbar to select assets.</p>
            }
          </div>
          <div className='map-container' aria-label='Asset Selection Map'>
            <BaseMap
              center={[41.8781, -87.6298]}
              zoom={11}
              whenCreated={onMapCreated}>
              {searchGeoms && 
                <>
                  <GeoJSON 
                    data={searchGeoms} 
                    // Hash key tells the geojson to re-render 
                    // when the state changes: https://stackoverflow.com/a/46593710
                    key={hash(searchGeoms)} 
                    style={{color: 'black', dashArray: '5,10', weight: '0.75'}}
                    onEachFeature={onEachFeature}
                  />
                    <MapClipper 
                      geoJson={searchGeoms}
                      onClipped={onClipped}
                    />
                    <MapZoom searchGeoms={searchGeoms} />
                </>
              }
              {existingGeoms && 
                <GeoJSON
                  data={existingGeoms} 
                  style={{color: 'green'}}
                  pointToLayer={pointToLayer}
                  onEachFeature={onEachFeature} />
              }
            </BaseMap>
          </div>
        </div>
      </div>
      <div>
        {existingGeoms && 
          <ExistingAssetsTable
            rows={existingGeoms.features}
          />
        }
      </div>
    </>
  )
}

ReactDOM.render(
  React.createElement(SelectAssetsMap, window.props),
  window.reactMount
)
