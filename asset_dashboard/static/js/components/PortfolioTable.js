import React from 'react'
import ReactTable from './BaseTable'

const PortfolioTable = ({ portfolioProjects, columns, onRemoveFromPortfolio, savePortfolio }) => {
  const onRowClick = ({ original }) => {
    return {
      onClick: e => {
        onRemoveFromPortfolio(original)
      }
    }
  }

  return (
    <div className="mb-5 mt-5">
      <h3>
        Portfolio
        <a href={`/`}
          onClick={savePortfolio}
          className='btn btn-primary float-right'>Save Portfolio</a>
      </h3>
      <ReactTable
        columns={columns}
        rows={portfolioProjects}
        getTrProps={onRowClick}
        rowClassNames='table-info'
        selector={() => {
          return (
            <span>
              <i className="fa fa-minus-square bg-"></i>
            </span>
          )
        }}
      />
    </div>
  )
}

export default PortfolioTable
