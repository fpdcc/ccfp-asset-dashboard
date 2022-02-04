import React from 'react'
import PropTypes from 'prop-types'
import Cookies from 'js-cookie'
import ReactTable from '../BaseTable'
import existingAssetsColumns from '../table_utils/existingAssetsColumns'
import renderMessage from '../helpers/renderMessage'

function ExistingAssetsTable({ rows }) {
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
        renderMessage('Assets successfully deleted.', 'success')
        location.reload()
      }
    }).catch(error => {
      renderMessage('An error occurred when deleting the asset. Please try again.', 'danger')
      console.error(error)
    })
  }

  return (
    <>
      <ReactTable
        rows={rows}
        columns={React.useMemo(() =>  existingAssetsColumns(handleDelete), [])}
        pageSizeIncrements={[10, 20, 30]}
        sizeOfPage={10}
      />
    </>
  )
}

ExistingAssetsTable.propTypes = {
  rows: PropTypes.array.isRequired
}

export default ExistingAssetsTable
