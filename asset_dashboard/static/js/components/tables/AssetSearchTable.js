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
    },
    {
      Header: 'Asset Type',
      accessor: 'properties.asset_type',
    }
  ]

  return (
    <>
      <ReactTable
        rows={rows}
        columns={React.useMemo(() => columns, [])}
        getTrProps={() => console.log('on row click')}
        pageSizeIncrements={[10]}
        sizeOfPage={7}
      />
    </>
  )
}

AssetSearchTable.propTypes = {
  rows: PropTypes.array.isRequired
}

export default AssetSearchTable
