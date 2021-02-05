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
        Header: <span>Name<i className="fas fa-sort ml-1 text-secondary"></i></span>,
        accessor: 'name',
        sortType: 'basic'
      },
      {
        Header: <span>Description<i className="fas fa-sort ml-1 text-secondary"></i></span>,
        accessor: 'projectDescription', 
      },
      {
        Header: <span>Total Score<i className="fas fa-sort ml-1 text-secondary"></i></span>,
        accessor: 'score',
      },
      {
        Header: <span>Total Budget<i className="fas fa-sort ml-1 text-secondary"></i></span>,
        accessor: 'budget',
      },
      {
        Header: () => null,
        accessor: 'linkTo',
        disableSortBy: true,
        Cell: props => <a href={props.value} 
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
