import React from 'react'

const PortfolioTotals = ({ portfolio }) => {
    return (
      <div className="row">
        <div className="mt-5 col">
          <h3>Projects</h3>
          <ul>
            {portfolio.map((project, index) => { return <li key={index}>{project.name || 'N/A'}</li> })}
          </ul>
        </div>

        <div className="mt-5 col">
          <h3>Zones</h3>
          <ul>
            {portfolio.map((project, index) => { return <li key={index}>{project.zone || 'N/A'}</li> })}
          </ul>
        </div>
        
        <div className="mt-5 col">
          <h3>Budget Impact</h3>
          <p>{portfolio.reduce((total, project) => { return total + project.budget }, 0) || null}</p>
        </div>
      </div>
    )
  }

export default PortfolioTotals