import React from "react"

// TODO come up with better name and move this file from the maps directory
export default function UpdateForm({ featureCollection, phases }) {

    function saveGeometries(geoms) {
        fetch(window.location.pathname, {
            headers: {
                'Cookie': document.cookie,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify(geoms)
        })
    }

    return (
        <div>
        <select>
            {/* TODO: select so they can associate with a phase...is this neccessary? */}
            {/* Do we need to associate an asset with a phase? How does this work when
                an asset will inevitably get added to every phase? */}
        </select>
        <button onClick={(featureCollection) => saveGeometries(featureCollection)}>
          Save Asset
        </button>
      </div>
    )
}
