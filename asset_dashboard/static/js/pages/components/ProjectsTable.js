import React from 'react'
import DataTable from 'react-data-table-component'

class ProjectsTable extends React.Component {
  constructor(props) {
    super(props)

    this.onSelectedChange = this.onSelectedChange.bind(this)
  }

  onSelectedChange({ selectedRows }) {
    // This event returns an array of all selected rows.
    // Any selected row will be added to the portfolio.
    // Iterate through the rows and change isDisabled
    // so that the portfolio table will know to render the row
    // as isDisabled.
    const projectsInPortfolio = selectedRows.map((project) => {
      return {
        ...project,
        isDisabled: !project.isDisabled
      }
    })

    // Send the array of selected rows to the parent component.
    // This will update the two tables and recalculate the budget impact.
    return this.props.onPortfolioChange(projectsInPortfolio)
  }

  render() {
    return (
      <>
        <DataTable
          columns={this.props.columns}
          data={this.props.allProjects}
          pagination
          keyField='key'
          striped
          noHeader
          noTableHead
          highlightOnHover
          pointerOnHover
          selectableRows
          selectableRowsHighlight
          onSelectedRowsChange={this.onSelectedChange}
          noContextMenu
        />
    </>
    )
  }
}

export default ProjectsTable