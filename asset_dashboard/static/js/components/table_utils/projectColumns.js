import React from 'react'

function createZoneNames(regions) {
  // returns an HTML-friendly list of names for the different regions/zones
  const names = regions.map(({ name }) => {
    return name
  }).join('\n')

  return names
}

const projectColumns = (selector) => {
  return [
    {
      Header: () => null,
      id: 'selector',
      Cell: props => selector(props.row.original),
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
      Header: 'Zones',
      accessor: 'zones',
      Cell: props => createZoneNames(props.value)
    },
    {
      Header: 'Phase',
      accessor: 'phase'
    },
    {
      Header: 'Year',
      accessor: 'year'
    },
    {
      Header: 'Quarter',
      accessor: 'estimated_bid_quarter'
    },
    {
      Header: 'Score',
      accessor: 'score',
    },
    {
      Header: 'Estimated Cost',
      accessor: 'budget',
      Cell: props => props.value.toLocaleString() // adds commas
    },
    {
      Header: 'Funded Amount',
      accessor: 'funded_amount',
      Cell: props => props.value.toLocaleString()
    },
    {
      Header: 'Funding',
      id: 'funding_streams',
      accessor: 'funding_streams',
      Cell: ({ row }) => (
        <span {...row.getToggleRowExpandedProps()}>
          {
            row.isExpanded ? 
              <button
                className='btn'
                type='button'
                aria-label="Hide funding">
                  <i className="fa fa-chevron-circle-up fa-lg"></i> 
              </button>
            : <button
                className='btn'
                type='button'
                aria-label="Show funding">
                  <i className="fa fa-chevron-circle-down fa-lg"></i>
            </button>
          }
        </span>
      ),
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
