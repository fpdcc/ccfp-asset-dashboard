import React, { useState, useEffect } from 'react'
import ApiService from './apiService'

export default function PromotePhaseForm({ phases, currentPhase, setAjaxMessage }) {
  const [selectedPhase, setSelectedPhase] = useState(null)
  
  useEffect(() => {
    setSelectedPhase(currentPhase)
  }, [currentPhase])

  function onPhaseChange(value) {
    setSelectedPhase(value)
  }
  
  function saveNewPhase() {
    const api = new ApiService({ onResponse: setAjaxMessage })
    
    const responseDetails = api.setNewPhase(selectedPhase, currentPhase)
  }

  return (
    <div class='col'>
      <div class='row'>
        <label className="h5">Copy Assets to Another Phase</label>
      </div>
      <div className='row'>
        <select className='form-control col' value={selectedPhase} onChange={(e) => onPhaseChange(e.target.value)}>
          {
            phases.map(phase => {
              let phaseName = ''
              if (phase.estimated_bid_quarter) {
                phaseName = `${phase.phase_type} - ${phase.estimated_bid_quarter} - ${phase.year} - ${phase.status}`
              } else {
                phaseName = `${phase.phase_type} - ${phase.year} - ${phase.status}`
              }
              return (
                <option value={phase.id} key={phase.id}>{phaseName}</option>
              )
            })
          }
        </select>
      </div>
      
      {
        (currentPhase !== selectedPhase) 
          ? <div className='row d-flex justify-content-center mt-2'>
              <button className="btn btn-info" onClick={saveNewPhase}>Copy Assets</button>
            </div>
          : null
      }
    </div>
  )
}