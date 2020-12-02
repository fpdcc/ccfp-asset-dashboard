import React from 'react'
import { useTable } from 'react-table'

const PortfolioTable = ({ portfolio = [],  getTrProps = props => props }) => {
    const columns = React.useMemo(
      () => [
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
          accessor: 'budget'
        }
      ], []
    )
  
    // Map the portfolio's projects to the array of rows.
    // The "accessor" value in the columns object ^ matches this object's keys.
    const data = React.useMemo(
      () => portfolio.map((project) => {
        return {
          projectDescription: project.project_description || 'No description available.',
          score: project.score || 'N/A',
          budget: project.budget || 0,
          key: project.key
        }
      }), [portfolio])
  
    const {
      getTableProps,
      getTableBodyProps,
      headerGroups,
      rows,
      prepareRow,
    } = useTable({ columns, data })
  
    return (
      <table {...getTableProps()} style={{ border: 'solid 1px gray' }}>
        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(column => (
                <th {...column.getHeaderProps()}>
                  {column.render('Header')}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
           {rows.map((row, i) => {
             prepareRow(row)
             return (
               <tr {...getTrProps(row.getRowProps(row))} key={i}>
                 {row.cells.map(cell => {
                   return (
                     <td
                       {...cell.getCellProps()}
                       style={{
                         padding: '10px',
                         border: 'solid 1px gray',
                         background: 'papayawhip',
                       }}
                     >
                       {cell.render('Cell')}
                     </td>
                   )
                 })}
               </tr>
             )
           })}
         </tbody>
      </table>
    )
  }

export default PortfolioTable