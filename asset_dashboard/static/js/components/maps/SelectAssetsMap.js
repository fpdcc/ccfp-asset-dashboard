import ReactDOM from 'react-dom'
import React, { useState, useEffect, useCallback } from 'react'
import { GeoJSON } from 'react-leaflet'
import hash from 'object-hash'
import Cookies from 'js-cookie'
import { useSessionstorageState } from 'rooks'
import * as turf from '@turf/turf'
import BaseMap from './BaseMap'
import AssetSearchTable from '../tables/AssetSearchTable'
import ExistingAssetsTable from '../tables/ExistingAssetsTable'
import GeometrySelector from '../map_utils/GeometrySelector'
import MapZoom from '../map_utils/MapZoom'
import zoomToSearchGeometries from '../map_utils/zoomToSearchGeometries'
import zoomToExistingGeometries from '../map_utils/zoomToExistingGeometries'
import Message from '../helpers/Message'
import bindPopup from '../map_utils/bindPopup'
import ShowPopup from '../map_utils/ShowPopup'
import circleMarker from '../map_utils/circleMarker'
import PromotePhaseForm from '../helpers/PromotePhaseForm'

function AssetTypeOptions() {
  const options = [
    {value: 'buildings', label: 'Buildings'},
    {value: 'trails', label: 'Trails'},
    {value: 'points_of_interest', label: 'Points of Interest'},
    {value: 'picnic_groves', label: 'Picnic Groves'},
    {value: 'parking_lots', label: 'Parking Lots'}
  ]

  return options.map(option => {
    return <option value={option.value} key={option.value}>{option.label}</option>
  })
}

function SelectAssetsMap(props) {
  const [searchGeoms, setSearchGeoms] = useSessionstorageState('searchGeoms', null)
  const [existingGeoms, setExistingGeoms] = useState()
  const [geomsToSave, setGeomsToSave] = useState(null)
  const [searchText, setSearchText] = useSessionstorageState('searchText', '')
  const [searchAssetType, setSearchAssetType] = useSessionstorageState('searchAssetTypes', 'buildings')
  const [isLoading, setIsLoading] = useState(false)
  const [isSavingAssets, setIsSavingAssets] = useState(false)
  const [phaseId, setPhaseId] = useState(null)
  const [ajaxMessage, setAjaxMessage] = useSessionstorageState('ajaxMessage', null)
  const [multipleFeatures, setMultipleFeatures] = useState(null)
  const [singleFeature, setSingleFeature] = useState(null)

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

  function onGeometriesSelected(featureCollection) {
    setMultipleFeatures(featureCollection)
  }

  function saveGeometries() {
    const existingIDs = existingGeoms?.features ? existingGeoms.features.map(geom => geom.properties.asset_id) : []

    let data = geomsToSave['features']
      .map(feature => {
        // Only include feature if it doesn't already exist
        if (!existingIDs.includes(feature.properties.identifier.toString())) {
          return {
            'asset_id': feature['properties']['identifier'],
            'asset_type': searchAssetType,
            'asset_name': feature['properties']['name'],
            'geom': feature['geometry'],
            'phase': phaseId
          }
        }
      }).filter(feature => {
        // map() adds 'undefined' if the conditional fails, so filter those out
        return feature !== undefined
      })

    if (data.length == 0) {
      setAjaxMessage({text: 'All selected assets already exist', tag: 'danger'})
      return
    }

    setIsSavingAssets(true)

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
      setIsSavingAssets(false)
      if (response.status == 201) {
        setAjaxMessage({text: 'Assets successfully saved.', tag: 'success'})
        location.reload()
      } else {
        response.json().then(errors => {
          let errorMessage = ''

          errors.forEach(error => {
            for (const [key, value] of Object.entries(error)) {
              errorMessage += `Error for field: ${key}. ${value.join(' ')}`
            }
          })

          setAjaxMessage({
            text: `An error occured saving the assets. ${errorMessage}`,
            tag: 'danger'
          })
        })
      }
    }).catch(error => {
      setAjaxMessage({text: 'An error occurred saving the selected assets. Please try again.', tag: 'danger'})
      console.error(error)
    })
  }

  function searchAssets() {
    setIsLoading(true)

    if (searchText.length == 0) {
      setAjaxMessage({text: 'Please enter a search query.', tag: 'danger'})
      return
    }

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

      if (data.features.length == 0) {
        setAjaxMessage({text: 'No assets found with search query.', tag: 'info'})
      }

      setSearchGeoms(data)
    })
    .catch(error => {
      setIsLoading(false)
      setAjaxMessage({text: 'An error occurred searching for assets. Please try again.', tag: 'danger'})
      console.error('error', error)
    })
  }

  function onSearchAssetClick(e) {
    const layer = e.target
    const layerFeature = layer?.feature ? layer.feature : null

    if (layerFeature) {
      setSingleFeature(layerFeature)
    }
  }

  /*
    The geometry features to save can come from three different user interactions:
      1. By clicking on a row in the search table. This loads up the singleFeature to save.
      2. By clicking on a single geom in the map. This also loads up the singleFeature to save.
      3. By selecting multipleFeatures via the GeometrySelector component, which loads multipleFeatures to save.
    If a user happens to select multipleFeatures and a singleFeature in one combination of interactions,
    then we need to save those pieces of states together. We also need to be able to save if they've been
    selected in separate interactions, like if a user only selects a single geometry features and clicks to
    save, or if they use the draw tool to select multiple features.

    In other words, we need to be able to handle when a user selects multipleFeatures and a singleFeature
    in the same interaction, without first pressing the "save" button when they switch between two types
    of interaction.

    To handle these variations, useEffect listens to changes to the singleFeature and multipleFeature
    variables. When either of those variables change, we reset the geomsToSave variable. The data
    in geomsToSave is what gets POSTed to the API.
  */
  useEffect(() => {
    let featureCollection = null

    if (multipleFeatures && singleFeature) {
      featureCollection = turf.featureCollection([singleFeature, ...multipleFeatures.features])
    } else if (multipleFeatures && !singleFeature) {
      featureCollection = multipleFeatures
    } else if (singleFeature && !multipleFeatures) {
      featureCollection = turf.featureCollection([singleFeature])
    }

    setGeomsToSave(featureCollection)
  }, [multipleFeatures, singleFeature])

  const onEachSearchFeature = useCallback(
    (feature, layer) => {
      bindPopup(feature, layer)

      layer.on({
        'click': onSearchAssetClick,
        'popupclose': () => {
          setSingleFeature(null)

          // Reset the fillColor because the layer changed color
          // whenever it was clicked on.
          if (layer.setStyle) {
            layer.setStyle({
              fillColor: 'black',
              fillOpacity: '0.2',
            })
          }
        }
      })
    }, [searchGeoms]
  )

  const onEachExistingAssetFeature = useCallback(
    (feature, layer) => {
      bindPopup(feature, layer)
    }, [existingGeoms]
  )

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
        <div className='col-4 bg-white border rounded border-secondary shadow-sm py-1 ml-3'>
          <div className='row my-3'>
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
                  onSelectRow={setSingleFeature}
                />
            }
          </div>
        </div>
        <div className='col'>
          <div className='card text-center bg-white mb-3 border-secondary shadow-sm'>
            <div className='card-body'>
                <div className='d-flex justify-content-start'>
                  <a href={`/projects/phases/edit/${phaseId}`} className='text-info lead'>{'<'} Back to phase</a>
                </div>
                <h2 className='card-title'>{props.phase_name}</h2>
                <div>
                  {geomsToSave
                    ?
                      <button
                        className='btn btn-info'
                        onClick={() => saveGeometries()}>
                        Add Asset to Phase
                      </button>
                    : <p className='lead'>Click on an asset or use the map toolbar to select and save assets.</p>
                  }
                  {
                    isSavingAssets
                      ? <div className='mt-3'>
                          <div class="spinner-border text-primary" role="status"></div>
                          <p>Assets are saving...</p>
                      </div>
                      : null
                  }
                </div>
            </div>
          </div>

          <div className='map-container bg-white border border-secondary rounded shadow-sm' aria-label='Asset Selection Map'>
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
                    style={{color: 'black', dashArray: '5,10', weight: '2'}}
                    onEachFeature={onEachSearchFeature}
                  />
                    <GeometrySelector
                      geoJson={searchGeoms}
                      onGeometriesSelected={onGeometriesSelected}
                    />
                    <MapZoom searchGeoms={searchGeoms} />
                    {/* {selectedSearchAsset && <ShowPopup geojson={selectedSearchAsset} />} */}
                    {singleFeature && <ShowPopup geojson={singleFeature} />}
                </>
              }
              {existingGeoms &&
                <GeoJSON
                  data={existingGeoms}
                  style={{color: 'green'}}
                  pointToLayer={circleMarker}
                  onEachFeature={onEachExistingAssetFeature} />
              }
            </BaseMap>
          </div>
        </div>
      </div>
      <div>

      <div className='row mt-3 mx-1'>
        <div className='col bg-white border rounded border-secondary shadow-sm'>
          <h3 className='m-3'>Phase Assets</h3>
          {
            existingGeoms
              ? <ExistingAssetsTable
                  rows={existingGeoms.features}
                  setAjaxMessage={setAjaxMessage}
                />
              : <p className='m-4'>Phase has no assets.</p>
          }
        </div>

        <div className='col-4 card bg-white border-secondary shadow-sm ml-3'>
          <div className='card-body'>
            <div className="d-flex flex-column">
              <div className='row d-flex flex-column'>
                <h4 className='card-title'>{props.phase_name}</h4>
              </div>
              <div className="row my-4">
                <PromotePhaseForm
                  phases={JSON.parse(props.phases)}
                  currentPhase={phaseId}
                  setAjaxMessage={setAjaxMessage} />
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>
    </>
  )
}

ReactDOM.render(
  React.createElement(SelectAssetsMap, window.props),
  window.reactMount
)
