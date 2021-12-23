import ReactDOM from 'react-dom'
import React, { useState, useEffect, useRef } from 'react'
import { GeoJSON, useMap } from 'react-leaflet'
import BaseMap from '../maps/base'


function UpdateMap(props) {
    const [ searchAssets, setSearchAssets ] = useState()
    const [ existingGeom, setExistingGeom ] = useState()
    const geoJsonRef = useRef()

    useEffect(() => {
        if (props?.search_assets) {
            setSearchAssets(JSON.parse(props.search_assets))
        }

        // TODO: implement this on the backend
        if (props?.existing_assets) {
            setExistingGeom(JSON.parse(props.existing_assets))
        }
    }, [setSearchAssets, setExistingGeom])

    function onMapCreated(map) {
        const group = new L.featureGroup

        map.eachLayer(layer => {
            if (layer.feature) {
                group.addLayer(layer)
            }
        })

        map.fitBounds(group.getBounds())
    }

    return (
        <div className='map-viewer'>
            <BaseMap center={[41.8781, -87.6298]} zoom={11} whenCreated={onMapCreated}>
                <GeoJSON data={searchAssets} />
            </BaseMap>
        </div>
    )
}

ReactDOM.render(
    React.createElement(UpdateMap, window.props),
    window.reactMount,
)