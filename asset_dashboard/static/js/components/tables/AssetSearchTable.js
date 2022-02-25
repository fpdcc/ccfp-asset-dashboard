import React from 'react'
import ReactTable from '../BaseTable'
import PropTypes from 'prop-types'
import assetSearchColumns from '../table_utils/assetSearchColumns'

function AssetSearchTable({ rows }) {
  return (
    <>
      <ReactTable
        rows={rows}
        columns={React.useMemo(() => assetSearchColumns, [])}
        // we could use this to select assets from the table
        getTrProps={() => console.log('on row click')} 
        pageSizeIncrements={[10]}
        sizeOfPage={10}
      />
    </>
  )
}

AssetSearchTable.propTypes = {
  rows: PropTypes.array.isRequired
}

export default AssetSearchTable
