import React from 'react'
import ReactTable from './BaseTable'
import projectColumns from './table_utils/projectColumns'

const ProjectsTable = ({ allProjects, onAddToPortfolio, searchInput }) => {
  const onRowClick = ({ original }) => {
    return {
      onClick: e => {
        onAddToPortfolio(original)
      }
    }
  }

  const selector = () => {
    return (
      <span>
        <i className="fas fa-plus-square"></i>
      </span>
    )
  }

  return (
    <>
      <div className="d-flex justify-content-between px-2">
        <h3>All Projects</h3>
        {searchInput}
      </div>
      
      <ReactTable
        rows={allProjects}
        columns={React.useMemo(() => projectColumns(selector), [])}
        getTrProps={onRowClick}
      />
    </>
  )
}

export default ProjectsTable
