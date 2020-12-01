import React from 'react'

const PortfolioTotals = ({ totals }) => {
    return (
      <div className="row">
        <div className="mt-5 col">
          <h3>Projects</h3>
          <ul>{totals.projectNames.map((name, index) => { return <li key={index}>{name || 'N/A'}</li> })}</ul>
        </div>

        <div className="mt-5 col">
          <h3>Zones</h3>
          <ul>
            {totals.projectZones.map((zone, index) => { return <li key={index}>{zone || 'N/A'}</li> })}
          </ul>
        </div>
        
        <div className="mt-5 col">
          <h3>Budget Impact</h3>
          <p>{totals.budgetImpact || null}</p>
        </div>
      </div>
    )
  }

export default PortfolioTotals