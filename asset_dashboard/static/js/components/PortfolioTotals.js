import React from 'react'

const PortfolioTotals = ({ totals }) => {
    return (
      <div className="mt-5">
        <div className="mt-2 col card shadow-sm pt-2 text-center">
          <h5>Budget Impact</h5>
          <h3>${totals.budgetImpact.toLocaleString() || 0}</h3>
        </div>

        <div className="mt-2 col card shadow-sm pt-2 text-center">
          <h5>Projects</h5>
          <ul className="list-unstyled">
            {totals.projectNames.length > 0 ?
              totals.projectNames.map(
                (name, index) => { 
                  return <li key={index}>{name || 'N/A'}</li>})
                  : 'N/A'
            }
          </ul>
        </div>

        <div className="mt-2 col card shadow-sm pt-2 text-center">
          <h5>Zones</h5>
          <ul className="list-unstyled">
            {
              totals.projectZones.length > 0 ?
                totals.projectZones.map((zone, index) => { 
                  return <li key={index}>{zone || 'N/A'}</li> })
                  : 'N/A'
            }
          </ul>
        </div>
      </div>
    )
  }

export default PortfolioTotals
