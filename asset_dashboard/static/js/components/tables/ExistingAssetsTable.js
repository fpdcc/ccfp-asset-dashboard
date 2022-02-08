import React, { useState } from 'react'
import PropTypes from 'prop-types'
import Cookies from 'js-cookie'
import ReactTable from '../BaseTable'
import existingAssetsColumns from '../table_utils/existingAssetsColumns'

function ExistingAssetsTable({ rows }) {
  const [ajaxMessage, setAjaxMessage] = useState(null)

  function handleDelete(assetId) {
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
      }
    }).catch(error => {
      setAjaxMessage('An error occurred when deleting the asset. Please try again.')
      console.error(error)
    })
  }

  return (
    <div>
      <h3>Phase Assets</h3>
      {ajaxMessage ? <p className='text-center alert alert-success'>{ajaxMessage}</p> : null}
      <ReactTable
        rows={rows}
        columns={React.useMemo(() =>  existingAssetsColumns(handleDelete), [])}
        pageSizeIncrements={[10, 20, 30]}
        sizeOfPage={10}
      />
    </div>
  )
}

ExistingAssetsTable.propTypes = {
  rows: PropTypes.array.isRequired
}

export default ExistingAssetsTable
