import React from 'react'
import ReactTable from './BaseTable'

const ProjectsTable = ({ allProjects, columns, onAddToPortfolio }) => {
  const onRowClick = ({ original }) => {
    return {
      onClick: e => {
        onAddToPortfolio(original)
      }
    }
  }

  return (
    <div className="mt-4">
      <h3>All Projects</h3>
      <ReactTable
        rows={allProjects}
        columns={columns}
        getTrProps={onRowClick}
        selector={() => {
          return (
            <span>
              <i className="fas fa-plus-square"></i>
            </span>
          )
        }} />
    </div>
  )
}

export default ProjectsTable