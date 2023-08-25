import React from 'react'

const TableFilter = ({ options, value, onChange, fieldName }) => {
  console.log('fieldName', fieldName)
  console.log(options)
  return (
    <div className="form-group">
      <label htmlFor={`${fieldName}-select`}>
        <h5>Filter by {fieldName}</h5>
      </label>
      <select
        id={`${fieldName}-select`}
        className="form-control"
        onChange={onChange}
        value={value ? value : ''}>
        <option value="">Show all</option>
        {options.map(option => {
          return <option key={option.value} value={option.value}>{option.label}</option>
        })}
      </select>
    </div>
  )
}

export default TableFilter
