import React, { useCallback, useEffect, useState } from 'react'
import ReactTable from '../BaseTable'
import PropTypes from 'prop-types'
import assetSearchColumns from '../table_utils/assetSearchColumns'

function AssetSearchTable({ rows, onSelectRow }) {
  const [columns, setColumns] = useState(assetSearchColumns)

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
    if (rows[0].properties.grove_number) {
      const newColumns = [
        {
          Header: 'Grove',
          accessor: 'properties.grove_number', 
        },
        ...columns
      ]
    
      setColumns(newColumns)
    }
    
    if (rows[0].properties.complex) {
      const newColumns = [
        ...columns, 
        {
          Header: 'Complex',
          accessor: 'properties.complex', 
        }
      ]
    
      setColumns(newColumns)
    }
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
