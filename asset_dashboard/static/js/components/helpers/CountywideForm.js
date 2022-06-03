import React, { useState, useEffect } from 'react'
import ApiService from './apiService'
import Message from './Message'

export default function CountywideForm({ currentCountywideValue, onCountywideChange, phaseId }) {
  const [isCountywide, setIsCountywide] = useState(currentCountywideValue)
  const [ajaxMessage, setAjaxMessage] = useState(null)

  function onCheckboxChange(event) {
    setIsCountywide(event.currentTarget.checked)
    onCountywideChange(event.currentTarget.checked)
  }
  
  function saveSelection() {
    const api = new ApiService(setAjaxMessage)
    api.saveCountywideSelection(isCountywide, phaseId)
  }

  return (
    <>
      {ajaxMessage 
        ? <Message 
            text={ajaxMessage.text} 
            messageTag={ajaxMessage.tag} 
            onCloseMessage={setAjaxMessage}
          /> 
        : null
      }
      
      <div className='col-4 border rounded border-secondary p-2 mx-2'>
        <div className='row'>
          <h6 className="col text-center"><strong>Countywide</strong></h6>
        </div>
        <div className='row d-flex flex-row justify-content-center align-items-center '>
          <label>Toggle for a countywide phase</label>
          <input type="checkbox" onChange={onCheckboxChange} checked={isCountywide} />
          <button className="btn btn-info" onClick={saveSelection}>Save</button>
        </div>
      </div>
    </>
  )
}