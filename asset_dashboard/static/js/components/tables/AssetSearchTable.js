import React, { useCallback, useEffect, useState } from 'react'
import ReactTable from '../BaseTable'
import PropTypes from 'prop-types'
import assetSearchColumns from '../table_utils/assetSearchColumns'
import makeColumns from '../table_utils/makeColumns'

function AssetSearchTable({ rows, onSelectRow }) {
  const [columns, setColumns] = useState([])

  const onRowClick = useCallback(
    ({ original }) => {
      return {
        onClick: e => {
          onSelectRow(original)
        }
      }
    }, [rows]
  )
  
  useEffect(() => {
    const newColumns = makeColumns(rows, assetSearchColumns)
    setColumns(newColumns)
  }, [rows])

  return (
    <div className='p-2'>
      <ReactTable
        rows={rows}
        columns={columns}
        getTrProps={onRowClick} 
        pageSizeIncrements={[10]}
        sizeOfPage={10}
        cellClassNames='text-nowrap'
      />
    </div>
  )
}

AssetSearchTable.propTypes = {
  rows: PropTypes.array.isRequired
}

export default AssetSearchTable
