import React from 'react'

const PortfolioPicker = ({ portfolios, changePortfolio }) => {
  return (
    <div className="form-group">
      <label htmlFor="portfolio-select" className="font-weight-bold">Select portfolio</label>
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
