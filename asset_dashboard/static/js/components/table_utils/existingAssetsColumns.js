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
      Cell: props => (<button onClick={() => handleDelete(props.value)}>Delete</button>)
    }
  ]
}

export default existingAssetsColumns

{/* <a href={`local-assets/${props.value}`}  
                        onClick={(e) => console.log('click', e.target.value)}
                        className='btn btn-success btn-sm'>Delete</a> */}
