import React, { useState, useEffect } from 'react'
import ReactDOM from 'react-dom'

import AssetsListMap from './maps/AssetsListMap'
import CountywideForm from './helpers/CountywideForm'

function PhaseDetailAssetTable(props) {
  const [phaseId, setPhaseId] = useState(null)
  const [isCountywide, setIsCountywide] = useState(null)
  
  useEffect(() => {
    if (props?.phase_id) {
      setPhaseId(props.phase_id)
    }
    
    setIsCountywide(props.is_countywide)
  }, [])

  return (
    <>
      <div className='row d-flex justify-content-between'>
        <div className="d-flex align-items-center justify-content-between m-2 col-4">
          <h3>Phase Assets</h3>
          <a href={`/projects/phases/edit/${phaseId}/assets`} class="text-info lead" style={isCountywide ? {pointerEvents: "none", opacity: "0.4"} : {}}>Edit Assets ></a>
        </div>
        {
          isCountywide !== null 
            ? <CountywideForm 
              currentCountywideValue={isCountywide} 
              phaseId={phaseId} />
            : null
        }
      </div>
      <div style={isCountywide ? {pointerEvents: "none", opacity: "0.4"} : {}} >
        <AssetsListMap assets={props.assets} />
      </div>
    </>
  )
}

ReactDOM.render(
  React.createElement(PhaseDetailAssetTable, window.props),
  window.reactMount
)