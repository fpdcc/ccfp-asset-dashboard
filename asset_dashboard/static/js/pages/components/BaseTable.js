import React from 'react'
import { useTable, usePagination } from 'react-table'

const BaseTable = ({ rows = [],  getTrProps = props => props, rowClassNames, selector }) => {
  const data = React.useMemo(
    () => rows.map((project) => {
      return project
    }), [rows])

  const columns = React.useMemo(
    () => [
      {
        Header: () => null,
        id: 'selector',
        Cell: selector ? selector : <span></span>
      },
      {
        Header: 'Project Description',
        accessor: 'projectDescription', 
      },
      {
        Header: 'Total Score',
        accessor: 'score',
      },
      {
        Header: 'Total Budget',
        accessor: 'budget',
      }
    ], []
  )

 

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    prepareRow,
    page,
    canPreviousPage,
    canNextPage,
    pageOptions,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    setPageSize,
    state: { pageIndex, pageSize },
  } = useTable({ columns, data, initialState: { pageIndex: 0, pageSize: 15 }}, usePagination)

  return (
    <div className="table-responsive">
      <table {...getTableProps()} className='table table-striped table-hover'>

        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()} className='col'>
              {headerGroup.headers.map(column => (
                <th {...column.getHeaderProps()}>
                  {column.render('Header')}
                </th>
              ))}
            </tr>
          ))}
        </thead>

        <tbody {...getTableBodyProps()}>
            {page.map((row, i) => {
              prepareRow(row)
              return (
                <tr {...getTrProps(row.getRowProps(row))} 
                    key={i} className={rowClassNames ? `${rowClassNames} cursor-pointer` : 'cursor-pointer'}>
                  {row.cells.map(cell => {
                    return (
                      <td {...cell.getCellProps()}>
                        {cell.render('Cell')}
                      </td>
                    )
                  })}
                </tr>
              )
            })}
          </tbody>
      </table>
      
      
      <div className="container">
        <nav aria-label="Pagination for all potential projects." className="row">
          <span className="col">
            Viewing {pageIndex + 1} of {pageOptions.length}
          </span>
          
          <ul className="pagination col">
            <li className="page-item">
              <button onClick={() => gotoPage(0)} disabled={!canPreviousPage} className="btn btn-light">
                {'<<'}
              </button>
            </li>
            <li className="page-item ml-2">
              <button onClick={() => previousPage()} disabled={!canPreviousPage} className="btn btn-light">
                {'<'}
              </button>
            </li>
            <li className="page-item ml-2">
              <button onClick={() => nextPage()} disabled={!canNextPage} className="btn btn-light">
                {'>'}
              </button>
            </li>
            <li className="page-item ml-2">
              <button onClick={() => gotoPage(pageCount - 1)} disabled={!canNextPage} className="btn btn-light">
                {'>>'}
              </button>
            </li>
          </ul>
          
          <div className="col w-25">
            <ul className="pagination col">
              Showing 
              {[15, 30, 45].map(pSize => (
                <li 
                  key={pSize} 
                  value={pSize} 
                  className="page-item ml-2"  
                  >
                  <button 
                    onClick={e => {
                      setPageSize(Number(pSize))
                    }}
                    className={`btn btn-light ${(pSize == pageSize) ? 'active' : '' }`}
                    >
                    {pSize}
                  </button>
                </li>
              ))}
              </ul>
          </div>
        </nav>
      </div>
    </div>
  )
}

export default BaseTable
