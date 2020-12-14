import React from 'react'
import ReactTable from './BaseTable'

const PortfolioTable = ({ portfolioProjects, columns, onRemoveFromPortfolio }) => {
  const onRowClick = ({ original }) => {
    return {
      onClick: e => {
        onRemoveFromPortfolio(original)
      }
    }
  }

  return (
    <>
      <ReactTable
        columns={columns}
        rows={portfolioProjects}
        getTrProps={onRowClick}
      />
    </>
  )
}

export default PortfolioTable