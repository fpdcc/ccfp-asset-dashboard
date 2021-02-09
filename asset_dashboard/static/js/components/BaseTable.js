import React from 'react'
import { useTable, usePagination, useSortBy } from 'react-table'

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
        Cell: selector ? selector : <span></span>,
        disableSortBy: true
      },
      {
        Header: 'Name',
        accessor: 'name'
      },
      {
        Header: 'Description',
        accessor: 'description', 
      },
      {
        Header: 'Total Score',
        accessor: 'score',
      },
      {
        Header: 'Total Budget',
        accessor: 'budget',
      },
      {
        Header: 'Phase',
        accessor: 'phase'
      },
      {
        Header: () => null,
        accessor: 'key',
        disableSortBy: true,
        Cell: props => <a href={`/projects/${props.value}`}  
                          onClick={e => e.stopPropagation()}
                          className='btn btn-success btn-sm'>View Project</a>
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
  } = useTable({ columns, data, initialState: { pageIndex: 0, pageSize: 15 }}, useSortBy, usePagination)

  const renderSorting = (column) => {
    if (column.isSorted) {
      return (
        <i className="fas fa-sort ml-1 text-secondary"></i>
      )
    } else {
      return null
    }
    
  }
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
                      <td {...cell.getCellProps()} className='text-center'>
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
          <div className="d-flex col justify-content-start align-items-center ml-2">
            <small className="text-muted">Pages {pageIndex + 1} of {pageOptions.length}</small>
          </div>
          
          <ul className="pagination col d-flex justify-content-center">
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
          
          <ul className="pagination col d-flex justify-content-end">
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
                  className={`btn btn-light btn-sm ${(pSize == pageSize) ? 'active' : '' }`}
                  >
                  {pSize}
                </button>
              </li>
            ))}
          </ul>
      </div>
    </div>
  )
}

export default BaseTable
