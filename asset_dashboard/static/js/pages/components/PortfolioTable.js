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

  const SelectorComponent = () => {
    return (
      <span>
        <i className="fas fa-minus"></i>
      </span>
    )
  }

  return (
    <div className="mb-5 mt-5">
      <h3>Portfolio</h3>
      <ReactTable
        columns={columns}
        rows={portfolioProjects}
        getTrProps={onRowClick}
        rowClassNames='table-info'
        selector={() => {
          return (
            <span>
              <i className="fa fa-minus-square"></i>
            </span>
          )
        }}
      />
    </div>
  )
}

export default PortfolioTable