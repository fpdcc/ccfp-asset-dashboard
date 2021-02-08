import React from 'react'
import ReactTable from './BaseTable'

const ProjectsTable = ({ allProjects, columns, onAddToPortfolio, searchInput }) => {
  const onRowClick = ({ original }) => {
    return {
      onClick: e => {
        onAddToPortfolio(original)
      }
    }
  }

  return (
    <>
      <div className="d-flex justify-content-between px-2">
        <h3>All Projects</h3>
        {searchInput}
      </div>
      
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
    </>
  )
}

export default ProjectsTable
