import React from 'react'

export default function PortfolioTotalsTable({ totals }) {
  return (
    <table class='table table-sm'>
      <thead>
        <tr>
          <th>Year</th>
          <th>Amount</th>
        </tr>
      </thead>
      <tbody>
        {
          Object.entries(totals).map(total => {
            return (
              <tr>
                <td>{total[0]}</td>
                <td>${total[1].toLocaleString()}</td>
              </tr>
            )
          })
        }
      </tbody>
    </table>
  )
}