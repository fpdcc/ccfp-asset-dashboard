import React from 'react'

const existingAssetsColumns = (handleDelete) => {
  let columns = [
    {
      Header: 'Identifier',
      accessor: 'properties.asset_id'
    },
    {
      Header: 'Name',
      accessor: 'properties.asset_name', 
    },
    {
      Header: 'Type',
      accessor: 'properties.asset_type'
    }
  ]

  if (handleDelete) {
    columns.push({
      Header: () => null,
      accessor: 'id',
      disableSortBy: true,
      Cell: props => (<button 
                        className='btn btn-outline-danger' 
                        onClick={() => handleDelete(props.value)}>
                          <i className='fas fa-trash'></i> Delete
                      </button>)
    })
  }

  return columns
}

export default existingAssetsColumns
