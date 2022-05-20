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
    const api = new ApiService(setAjaxMessage)
    
    const responseDetails = api.setNewPhase(selectedPhase, currentPhase, setAjaxMessage)
  }

  return (
    <div class="col">
      <div>
        <label className="row">Promote Assets to New Phase</label>
      </div>
      <div className='row'>
        <select className='form-control col-6 mr-1' value={selectedPhase} onChange={(e) => onPhaseChange(e.target.value)}>
          {
            phases.map(phase => {
              const phaseName = `${phase.phase_type} - ${phase.estimated_bid_quarter} - ${phase.year} - ${phase.status}`
              return (
                <option value={phase.id} key={phase.id}>{phaseName}</option>
              )
            })
          }
        </select>
        
        {
          (currentPhase !== selectedPhase) 
            ? <button className="btn btn-info" onClick={saveNewPhase}>Promote Phase</button>
            : null
        }
      </div>
    </div>
  )
}