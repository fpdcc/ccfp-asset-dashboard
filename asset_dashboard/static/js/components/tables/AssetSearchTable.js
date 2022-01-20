import React from 'react'
import ReactTable from '../BaseTable'
import PropTypes from 'prop-types'

function AssetSearchTable({ rows }) {

  const columns = [
    {
      Header: 'Identifier',
      accessor: 'properties.identifier'
    },
    {
      Header: 'Name',
      accessor: 'properties.name', 
    }
  ]

  return (
    <>
      <ReactTable
        rows={rows}
        columns={React.useMemo(() => columns, [])}
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
