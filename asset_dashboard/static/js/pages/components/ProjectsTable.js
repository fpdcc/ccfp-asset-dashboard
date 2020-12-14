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
    <>
      <ReactTable
        rows={allProjects}
        columns={columns}
        getTrProps={onRowClick} />
    </>
  )
}

export default ProjectsTable