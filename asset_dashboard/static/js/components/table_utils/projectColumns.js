import React from 'react'

const selector = () => {
    return (
      <span>
        <i className="fa fa-minus-square bg-"></i>
      </span>
    )
  }

const projectColumns = [
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
      Cell: props => <a href={`/projects/${props.value}`}  
                        onClick={e => e.stopPropagation()}
                        className='btn btn-success btn-sm'>View Project</a>
    }
  ]

export default projectColumns
