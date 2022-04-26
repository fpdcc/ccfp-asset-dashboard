import React from 'react'

export default function PortfolioTotalsTable({ totals, headers }) {
  return (
    <table class='table table-sm'>
      <thead>
        <tr>
          {
            headers.map(header => {
              return (<th>{header}</th>)
            })
          }
        </tr>
      </thead>
      <tbody>
        {
          Object.entries(totals).map(total => {
            return (
              <tr>
                <td>{total[0]}</td>
                <td>${Math.round(total[1]).toLocaleString()}</td>
              </tr>
            )
          })
        }
      </tbody>
    </table>
  )
}