import React, { useState, useEffect } from 'react'
import ApiService from './apiService'
import Message from './Message'

export default function CountywideForm({ currentCountywideValue, phaseId }) {
  const [isCountywide, setIsCountywide] = useState(currentCountywideValue)
  const [ajaxMessage, setAjaxMessage] = useState(null)

  function onCheckboxChange(event) {
    setIsCountywide(event.currentTarget.checked)
  }
  
  function saveSelection() {
    const api = new ApiService({ onResponse: setAjaxMessage })
    api.saveCountywideSelection(isCountywide, phaseId)
  }

  return (
    <div className='d-flex justify-content-center col'>
      <div className='col-5 border rounded border-secondary p-2 mx-2'>
        <div className='row'>
          <h6 className="col text-center"><strong>Countywide</strong></h6>
        </div>
        <div className='row d-flex flex-row justify-content-center align-items-center '>
          <label className='mb-1'>Set phase as {isCountywide ? 'not' : ''} countywide:</label>
          <input type="checkbox" onChange={onCheckboxChange} checked={isCountywide} />
          <button className="btn btn-info" onClick={saveSelection}>Save</button>
        </div>
        
        {ajaxMessage 
          ? <div className='m-2'>
              <Message 
                  text={ajaxMessage.text} 
                  messageTag={ajaxMessage.tag} 
                  onCloseMessage={setAjaxMessage}
                /> 
            </div>
          : null
        }
      </div>
    </div>
  )
}