import React, { useState } from 'react'
import Cookies from 'js-cookie'
import renderMessage from '../helpers/renderMessage'

const existingAssetsColumns = () => {
  const [ajaxMessage, setAjaxMessage] = useState(null)

  function handleDelete(assetId) {
    console.log('handld delete')
    fetch(`/local-assets/${assetId}`, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFTOKEN': Cookies.get('csrftoken')
      },
      method: 'DELETE',
      mode: 'same-origin'
    }).then((response) => {
      console.log('response', response)
      if (response.status == 204) {
        setAjaxMessage('Asset successfully deleted.')
        location.reload()
      } else {
        renderMessage('An error occurred when deleting the asset. Please try again.', 'danger')
      }
    }).catch(error => {
      renderMessage('An error occurred when deleting the asset. Please try again.', 'danger')
      console.error(error)
    })
  }

  return [
    {
      Header: 'Identifier',
      accessor: 'properties.asset_id'
    },
    {
      Header: 'Name',
      accessor: 'properties.asset_name', 
    },
    {
      Header: 'Type',
      accessor: 'properties.asset_type'
    },
    {
      Header: () => null,
      accessor: 'id',
      disableSortBy: true,
    Cell: props => (ajaxMessage 
                      ? <p>{ajaxMessage}</p>
                      : <button 
                        className='btn btn-outline-danger' 
                        onClick={() => handleDelete(props.value)}>
                          <i className='fas fa-trash'></i> Delete
                      </button>)
    }
  ]
}

export default existingAssetsColumns
