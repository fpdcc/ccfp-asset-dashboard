import React from 'react'
import { useTable, usePagination, useSortBy } from 'react-table'

const BaseTable = ({ rows = [], columns, getTrProps = props => props, rowClassNames, cellClassNames, sizeOfPage=15, pageSizeIncrements=[15, 30, 45] }) => {

  const data = React.useMemo(
    () => rows.map((row) => {
      return row
    }), [rows])

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
  } = useTable({ columns, data, initialState: { pageIndex: 0, pageSize: sizeOfPage }}, useSortBy, usePagination)

  return (
    <div className="table-responsive">
      <table {...getTableProps()} className='table table-striped table-hover'>

        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()} className='col'>
              {headerGroup.headers.map(column => (
                <th {...column.getHeaderProps(column.getSortByToggleProps())} className='text-center'>
                  {column.render('Header')}
                  {column.isSorted ? <span><i className="fas fa-sort ml-1 text-secondary"></i></span> : ''}
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
                      <td {...cell.getCellProps()} className={`${cellClassNames && cellClassNames} text-center`}>
                        {cell.render('Cell')}
                      </td>
                    )
                  })}
                </tr>
              )
            })}
          </tbody>
      </table>
      
      
      <div className="row container" aria-label="Pagination for all potential projects.">
          <div className="d-flex col align-items-center ml-2">
            <small className="text-muted mb-3">Pages {pageIndex + 1} of {pageOptions.length > 0 ? pageOptions.length : 1 }</small>
          </div>
          <ul className="pagination col d-flex align-items-center justify-content-center">
            <li className="page-item">
              <button onClick={() => gotoPage(0)} disabled={!canPreviousPage} className="btn btn-light btn-sm">
                {'<<'}
              </button>
            </li>
            <li className="page-item ml-2">
              <button onClick={() => previousPage()} disabled={!canPreviousPage} className="btn btn-light btn-sm">
                {'<'}
              </button>
            </li>
            <li className="page-item ml-2">
              <button onClick={() => nextPage()} disabled={!canNextPage} className="btn btn-light btn-sm">
                {'>'}
              </button>
            </li>
            <li className="page-item ml-2">
              <button onClick={() => gotoPage(pageCount - 1)} disabled={!canNextPage} className="btn btn-light btn-sm">
                {'>>'}
              </button>
            </li>
          </ul>
          
          {pageSizeIncrements.length > 1 &&
            <ul className="pagination col d-flex justify-content-end">
              {
                pageSizeIncrements.map(pSize => (
                  <li 
                    key={pSize} 
                    value={pSize} 
                    className="page-item ml-2"  
                    >
                    <button 
                      onClick={e => {
                        setPageSize(Number(pSize))
                      }}
                      className={`btn btn-light btn-sm ${(pSize == pageSize) ? 'active' : '' }`}
                      >
                      {pSize}
                    </button>
                  </li>
                ))
              }
            </ul>
          }
      </div>
    </div>
  )
}

export default BaseTable
