import React from 'react'
import ReactTable from './BaseTable'
import projectColumns from './table_utils/projectColumns'
import SubRow from './table_utils/SubRow'

const ProjectsTable = ({ allProjects, onAddToPortfolio, searchInput }) => {
  const Selector = (row) => {
    return (
      <button 
        class='btn'
        type='button'
        onClick={() => onAddToPortfolio(row)}>
        <i className="fas fa-plus-square fa-lg" aria-label='Add project to portfolio.'></i>
      </button>
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
        columns={React.useMemo(() => projectColumns(Selector), [])}
        renderRowSubComponent={React.useCallback(SubRow, [])}
      />
    </>
  )
}

export default ProjectsTable
