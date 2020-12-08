import React, { useState } from 'react'
import DataTable from 'react-data-table-component'
import styled from 'styled-components';

const TextField = styled.input`
  height: 32px;
  width: 400px;
  border-radius: 3px;
  border-top-left-radius: 5px;
  border-bottom-left-radius: 5px;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  border: 1px solid #e5e5e5;
  padding: 0 32px 0 16px;

  &:hover {
    cursor: pointer;
  }
`;

const customStyles = {
  header: {
    width: '50%'
  }
}

const FilterComponent = ({ filterText, onFilter }) => {
  return (
    <div className="mb-4">
      <p>Search for projects by name</p>
      <TextField 
        id="search" 
        type="text" 
        placeholder="Search" 
        aria-label="Search Input" 
        value={filterText} 
        onChange={onFilter} />
    </div>
  )
}

const PortfolioTable = ({ projects = [], onUpdatePortfolio }) => {
  const [filterText, setFilterText] = useState('')
  
  const columns = React.useMemo(
    () => [
      {
        name: 'Project Description',
        selector: 'projectDescription', 
        sortable: true,
        maxWidth: '550px'
      },
      {
        name: 'Total Score',
        selector: 'score',
        sortable: true,
        maxWidth: '50px',
      },
      {
        name: 'Total Budget',
        selector: 'budget',
        sortable: true,
        maxWidth: '75px'
      }
    ], []
  )

  const data = React.useMemo(
    () => projects.map((project) => {
      return {
        projectDescription: project.project_description || 'No description available.',
        score: project.score || 'N/A',
        budget: project.budget || 0,
        key: project.key,
        name: project.name,
        zone: project.zone
      }
    }), [projects])

  const filteredItems = data.filter(project => {
    return project.projectDescription.toLowerCase().includes(filterText.toLowerCase())
  })

  return (
    <>
      <div className="table-responsive">
        <DataTable
          columns={columns}
          data={filteredItems}
          pagination
          keyField='key'
          striped
          highlightOnHover
          pointerOnHover
          subHeaderAlign='left'
          subHeader
          subHeaderComponent={<FilterComponent onFilter={e => setFilterText(e.target.value)} filterText={filterText} />}
          selectableRows
          selectableRowsHighlight
          Clicked
          Selected
          onSelectedRowsChange={(row) => onUpdatePortfolio(row.selectedRows)}
          persistTableHead
          customStyles={customStyles}
          noContextMenu
        />  
      </div>
    </>
  )
}

export default PortfolioTable