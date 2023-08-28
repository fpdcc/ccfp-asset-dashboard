import React from 'react'

const PortfolioPicker = ({ portfolios, activePortfolio, changePortfolio }) => {
  return (
    <div className="col form-group mb-0">
      <label htmlFor="portfolio-select">
        <h5>Select portfolio</h5>
      </label>
      <select
        id="portfolio-select"
        className="form-control"
        onChange={changePortfolio}
        value={activePortfolio.id ? activePortfolio.id : ''}>
        <option value="">---</option>
        {portfolios.map(portfolio => {
          return <option key={portfolio.id} value={portfolio.id}>{portfolio.name}</option>
        })}
      </select>
    </div>
  )
}

export default PortfolioPicker
