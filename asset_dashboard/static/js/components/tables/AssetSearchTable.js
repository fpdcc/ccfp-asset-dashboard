import React, { useCallback } from 'react'
import ReactTable from '../BaseTable'
import PropTypes from 'prop-types'
import assetSearchColumns from '../table_utils/assetSearchColumns'

function AssetSearchTable({ rows, onSelectRow }) {
  const onRowClick = useCallback(
    ({ original }) => {
      return {
        onClick: e => {
          console.log('e', e)
          console.log('original', original)
          onSelectRow(original)
        }
      }
    }, [rows]
  )
  // const onRowClick = ({ original }) => {
  //   return {
  //     onClick: e => {
  //       console.log('e', e)
  //       console.log('original', original)
  //       onSelectRow(original)
  //     }
  //   }
  // }

  return (
    <>
      <ReactTable
        rows={rows}
        columns={React.useMemo(() => assetSearchColumns, [])}
        getTrProps={onRowClick} 
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
