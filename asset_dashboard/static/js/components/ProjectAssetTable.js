import React from 'react'
import ReactDOM from 'react-dom'
import AssetsListMap from './maps/AssetsListMap'

function PhaseAssetTable(props) {
  return (
    <div>
      <div className="d-flex align-items-center justify-content-between m-2 col-4">
        <h3>Project Assets</h3>
        <a href={`/projects/phases/edit/${props.assets.features[0].properties.phase}/assets`} class="text-info lead">Edit Assets ></a>
      </div>
      <AssetsListMap assets={props.assets} />
    </div>
  )
}

ReactDOM.render(
  React.createElement(PhaseAssetTable, window.props),
  window.reactMount
)