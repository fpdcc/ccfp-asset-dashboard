import React from 'react'

export default function SubRow({ row }) {
  const funding = row.values.funding_streams
  return (
    <div className='d-flex justify-content-center'>
      <table className='table table-sm w-75 table-bordered table-light'>
        <thead className='thead-dark'>
          <tr>
            <th>Year</th>
            <th>Amount</th>
            <th>Source</th>
            <th>Secured</th>
          </tr>
        </thead>
        <tbody>
          {
            funding.map(source => {
              return (
                <tr>
                  <td>{source.year}</td>
                  <td>{source.budget}</td>
                  <td>{source.source_type}</td>
                  <td>{source.funding_secured ? 'Yes' : 'No'}</td>
                </tr>
              )
            })
          }
        </tbody>
      </table>
    </div>
  )
}