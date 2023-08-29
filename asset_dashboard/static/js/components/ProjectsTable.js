import React from 'react'
import ReactTable from './BaseTable'
import projectColumns from './table_utils/projectColumns'
import SubRow from './table_utils/SubRow'

const ProjectsTable = ({ allProjects, onAddToPortfolio }) => {
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
      <ReactTable
        rows={allProjects}
        columns={React.useMemo(() => projectColumns(Selector), [])}
        renderRowSubComponent={React.useCallback(SubRow, [])}
      />
    </>
  )
}

export default ProjectsTable
