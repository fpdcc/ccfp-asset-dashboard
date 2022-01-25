import React from 'react'

const PortfolioPicker = ({ portfolios, changePortfolio }) => {
  return (
    <select
      className="form-control form-control-lg"
      onChange={changePortfolio}>
      {portfolios.map(portfolio => {
        return <option key={portfolio.id} value={portfolio.id}>{portfolio.name}</option>
      })}
    </select>
  )
}

export default PortfolioPicker
