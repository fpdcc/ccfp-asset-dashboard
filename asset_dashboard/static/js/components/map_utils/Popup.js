import React, { useRef } from 'react'
import deleteLocalAsset from '../helpers/deleteLocalAsset'

function Popup({ feature }) {
  return (
    <>
      {feature.properties &&
        <div>
          <ul className='col'>
            <li>{feature.properties.asset_id}</li>
            <li>{feature.properties.asset_name}</li>
            <li>{feature.properties.asset_type}</li>
          </ul>
        </div>
      }
    </>
  )
}

export default Popup
