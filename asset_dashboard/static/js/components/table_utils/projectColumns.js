import React from 'react'

const projectColumns = (selector) => {
  return [
    {
      Header: () => null,
      id: 'selector',
      Cell: selector ? selector : <span></span>,
      disableSortBy: true
    },
    {
      Header: 'Name',
      accessor: 'name'
    },
    {
      Header: 'Description',
      accessor: 'description', 
    },
    {
      Header: 'Total Score',
      accessor: 'score',
    },
    {
      Header: 'Total Budget',
      accessor: 'budget',
    },
    {
      Header: 'Phase',
      accessor: 'phase'
    },
    {
      Header: () => null,
      accessor: 'key',
      disableSortBy: true,
      Cell: props => <a href={`/projects/phases/edit/${props.value}/`}  
                        onClick={e => e.stopPropagation()}
                        className='btn btn-outline-dark btn-sm'
                        target="_blank">View Phase</a>
    }
  ]
}

export default projectColumns
