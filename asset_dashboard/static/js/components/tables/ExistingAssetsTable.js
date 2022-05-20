import React, { useState } from 'react'
import PropTypes from 'prop-types'
import Cookies from 'js-cookie'
import { useSessionstorageState } from 'rooks'
import ReactTable from '../BaseTable'
import existingAssetsColumns from '../table_utils/existingAssetsColumns'
import Message from '../helpers/Message'

function ExistingAssetsTable({ rows, setAjaxMessage }) {

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
      if (response.status == 204) {
        setAjaxMessage({text: 'Asset successfully deleted.', tag: 'success'})
        location.reload()
      }
    }).catch(error => {
      setAjaxMessage({text: 'An error occurred when deleting the asset. Please try again.', tag: 'danger'})
      console.error(error)
    })
  }

  return (
    <ReactTable
      rows={rows}
      columns={React.useMemo(() =>  existingAssetsColumns(handleDelete), [])}
      pageSizeIncrements={[10, 20, 30]}
      sizeOfPage={10}
    />
  )
}

ExistingAssetsTable.propTypes = {
  rows: PropTypes.array.isRequired
}

export default ExistingAssetsTable
