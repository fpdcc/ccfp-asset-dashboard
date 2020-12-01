import React from 'react'
import Select from 'react-select'

const SearchProjects = ({ projects, onSelection }) => {
    const options = projects && projects.map((project) => {
      return {
        value: project.key,
        label: project.name
      }
    })
  
      function onProjectSelection(project) {
        onSelection(project)
      }
  
    return (
      <div className="col-6">
        <Select 
          options={options}
          onChange={onProjectSelection}
        />
      </div>
    )
  }

export default SearchProjects
