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

  const savePortfolio = (event, portfolioProjects) => {
    event.preventDefault()
    console.log(portfolioProjects)
    // fetch create
    // show message depending on response
  }

  return (
    <div className="mb-5 mt-5">
      <h3>Portfolio</h3>
      <a href={`/`}
        onClick={e => savePortfolio(event, { portfolioProjects })}
        className='btn btn-success btn-sm'>Save Portfolio</a>
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
