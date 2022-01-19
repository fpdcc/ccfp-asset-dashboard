import React from 'react'
import ReactTable from './BaseTable'
import columns from './table-utils/projectColumns'

const PortfolioTable = ({ portfolioProjects, onRemoveFromPortfolio }) => {
  const onRowClick = ({ original }) => {
    return {
      onClick: e => {
        onRemoveFromPortfolio(original)
      }
    }
  }

  return (
    <div className="mb-5 mt-5">
      <h3>Portfolio</h3>
      <ReactTable
        columns={React.useMemo(() => columns, [])}
        rows={portfolioProjects}
        getTrProps={onRowClick}
        rowClassNames='table-info'
      />
    </div>
  )
}

export default PortfolioTable
