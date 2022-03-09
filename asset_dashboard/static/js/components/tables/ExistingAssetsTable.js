import React, { useState } from 'react'
import PropTypes from 'prop-types'
import Cookies from 'js-cookie'
import { useSessionstorageState } from 'rooks'
import ReactTable from '../BaseTable'
import existingAssetsColumns from '../table_utils/existingAssetsColumns'
import Message from '../helpers/Message'

function ExistingAssetsTable({ rows }) {
  const [ajaxMessage, setAjaxMessage] = useSessionstorageState('ajaxMessageTable', null)

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
        setAjaxMessage({text: 'Asset successfully deleted.', tag: 'success'})
        location.reload()
      }
    }).catch(error => {
      setAjaxMessage({text: 'An error occurred when deleting the asset. Please try again.', tag: 'danger'})
      console.error(error)
    })
  }

  return (
    <div className='border rounded border-secondary shadow-sm mt-4'>
      <h3 className='m-3'>Phase Assets</h3>
      {ajaxMessage 
        ? <Message
            text={ajaxMessage.text}
            messageTag={ajaxMessage.tag}
            onCloseMessage={setAjaxMessage}
          />
        : null
      }
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
