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

  return (
    <>
      <div className="d-flex justify-content-between px-2">
        <h3>All Projects</h3>
        {searchInput}
      </div>
      
      <ReactTable
        rows={allProjects}
        columns={React.useMemo(() => projectColumns, [])}
        getTrProps={onRowClick}
      />
    </>
  )
}

export default ProjectsTable
