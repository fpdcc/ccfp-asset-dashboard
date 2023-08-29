import React from 'react'

const TableFilter = ({ options, value, onChange, fieldName, label }) => {
  return (
    <div className="form-group col">
      <label htmlFor={`${fieldName}-select`}>
        <h5>{label}</h5>
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
