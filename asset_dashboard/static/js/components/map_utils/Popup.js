import React from 'react'

function Popup({ feature }) {
  const properties = feature.properties
  return (
    <>
      {properties &&
        <div>
          <h6>Asset Info</h6>
          <ul className='list-group list-group-flush'>
            <li className='list-group-item'>
              <strong>ID:</strong> {properties.asset_id ? properties.asset_id : properties.identifier }
            </li>
            <li className='list-group-item'>
              <strong>Name:</strong> {properties.asset_name ? properties.asset_name : properties.name }
            </li>
            {properties.asset_type 
              && <li className='list-group-item'>
                  <strong>Asset Type:</strong> {properties.asset_type}
                </li>
            }
          </ul>
        </div>
      }
    </>
  )
}

export default Popup
