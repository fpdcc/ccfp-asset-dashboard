import React from 'react'

const existingAssetsColumns = (handleDelete) => {
  return [
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
    },
    {
      Header: () => null,
      accessor: 'id',
      disableSortBy: true,
      Cell: props => (<button 
                        className='btn btn-outline-danger' 
                        onClick={() => handleDelete(props.value)}>
                          <i className='fas fa-trash'></i> Delete
                      </button>)
    }
  ]
}

export default existingAssetsColumns
