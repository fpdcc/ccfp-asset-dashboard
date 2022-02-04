import React from 'react'

const PortfolioPicker = ({ portfolios, changePortfolio }) => {
  return (
    <div className="form-group">
      <label htmlFor="portfolio-select">
        <h5>Select portfolio</h5>
      </label>
      <select
        id="portfolio-select"
        className="form-control"
        onChange={changePortfolio}>
        {portfolios.map(portfolio => {
          return <option key={portfolio.id} value={portfolio.id}>{portfolio.name}</option>
        })}
      </select>
    </div>
  )
}

export default PortfolioPicker
