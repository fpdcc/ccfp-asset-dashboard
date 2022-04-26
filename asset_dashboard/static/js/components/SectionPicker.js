import React from 'react'

const SectionPicker = ({ sections, activeSection, changeSection }) => {
  return (
    <div className="form-group">
      <label htmlFor="section-select">
        <h5>Filter by Section</h5>
      </label>
      <select
        id="section-select"
        className="form-control"
        onChange={changeSection}
        value={activeSection ? activeSection : ''}>
        <option value="">All Sections</option>
        {sections.map(section => {
          console.log('section', section)
          return <option key={section} value={section}>{section}</option>
        })}
      </select>
    </div>
  )
}

export default SectionPicker