import React from 'react'
import DataTable from 'react-data-table-component'

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
            />
        </>
    )
}

export default PortfolioTable