import React from 'react'
import PropTypes from 'prop-types'
import Cookies from 'js-cookie'
import ReactTable from '../BaseTable'
import existingAssetsColumns from '../table_utils/existingAssetsColumns'

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
        // TODO: this reloads the page but clears the user search...
        // Need to come up with way to reload by rehydrating the previous state
        location.reload()
        // TODO: show success message
        // https://stackoverflow.com/questions/13256817/django-how-to-show-messages-under-ajax-function
      }
    }).catch(error => {
      // TODO show error message
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
