import React from 'react'
import DataTable from 'react-data-table-component'

const tableStyles = {
    header: {
        style: {
          minHeight: '10px',
        }
}}

const PortfolioTable = ({ portfolioProjects, columns }) => {
    return (
        <>
            <DataTable 
                columns={columns}
                data={portfolioProjects}
                keyField='key'
                persistTableHead
                noDataComponent={<p>Select a project to update the portfolio.</p>}
                selectableRows
                selectableRowDisabled={row => row.isDisabled}
                noContextMenu
                customStyles={tableStyles}
            />
        </>
    )
}

export default PortfolioTable