import React, { useState, useEffect } from 'react'
import ApiService from './apiService'

export default function CountywideForm({ currentCountywideValue, onCountywideChange, phaseId, onResponse }) {
  const [isCountywide, setIsCountywide] = useState(currentCountywideValue)

  function onCheckboxChange(event) {
    setIsCountywide(event.currentTarget.checked)
    onCountywideChange(event.currentTarget.checked)
  }
  
  function saveSelection() {
    const api = new ApiService(onResponse)
    api.saveCountywideSelection(isCountywide, phaseId)
  }

  return (
    <div className='border rounded border-secondary p-4 text-center'>
      <h6><strong>Countywide</strong></h6>
      <label>Toggle for a countywide phase</label>
      <input type="checkbox" onChange={onCheckboxChange} checked={isCountywide} />
      <button className="btn btn-info" onClick={saveSelection}>Save</button>
    </div>
  )
}