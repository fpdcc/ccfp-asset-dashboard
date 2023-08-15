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
      Header: 'Funding source',
      id: 'funding_source',
      accessor: 'funding_source'
    },
    {
      Header: 'Funding amount',
      id: 'funding_amount',
      accessor: 'funding_amount',
      Cell: props => props.value.toLocaleString()
    },
    {
      Header: 'Funding year',
      id: 'funding_year',
      accessor: 'funding_year'
    },
    {
      Header: 'Funding secured',
      id: 'funding_secured',
      accessor: 'funding_secured',
    },
    {
      Header: 'Quarter',
      accessor: 'estimated_bid_quarter'
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
      Header: 'Score',
      accessor: 'score',
    },
    {
      Header: 'Description',
      accessor: 'description',
      Cell: props => (
        <>
          <button className="btn btn-outline-primary" type="button" data-toggle="collapse" data-target={`#toggleDescription-${props.row.id}`} aria-expanded="false" aria-controls="toggleDescription">
            Show/hide
          </button>

          <div className="collapse" id={`toggleDescription-${props.row.id}`}>
            <div className="card card-body">
              {props.value}
            </div>
          </div>
        </>
      )
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
