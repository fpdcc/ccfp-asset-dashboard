import React from 'react'

const Button = ({ onClick, children }) => {
  return (
      <button type="buton" className="btn btn-primary" onClick={onClick}>
          {children}
      </button>
  )
}

const AddProjectToPlan = ({ project, addProjectOnClick }) => {
  return (
    <>
      {project ? <p>{project.name} | {project.budget} | <Button onClick={(project) => addProjectOnClick(project)}>Add to Plan</Button></p>
              : null
      }
    </>
  )
}

export default AddProjectToPlan