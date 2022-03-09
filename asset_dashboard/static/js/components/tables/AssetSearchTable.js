import React, { useCallback } from 'react'
import ReactTable from '../BaseTable'
import PropTypes from 'prop-types'
import assetSearchColumns from '../table_utils/assetSearchColumns'

function AssetSearchTable({ rows, onSelectRow }) {
  const onRowClick = useCallback(
    ({ original }) => {
      return {
        onClick: e => {
          onSelectRow(original)
        }
      }
    }, [rows]
  )

  return (
    <div className='p-2'>
      <ReactTable
        rows={rows}
        columns={React.useMemo(() => assetSearchColumns, [])}
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
