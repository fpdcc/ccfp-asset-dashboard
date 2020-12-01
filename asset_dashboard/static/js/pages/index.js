import React, { useState, useEffect } from 'react'
import ReactDOM from 'react-dom'
import SearchProjects from './SearchProjects'
import PortfolioTable from './PortfolioTable'
import PortfolioTotals from './PortfolioTotals'
import AddProjectToPlan from './AddProjectToPlan'

const Dashboard = (props) => {  
  const [allProjects, setAllProjects] = useState([])
  const [potentialProject, setPotentialProject] = useState(null)
  const [portfolio, setPortfolio] = useState({projects: []})

  useEffect(() => {
    // Parse the props JSON string into an array of objects, 
    // then map each object to a new array.
    const projects = JSON.parse(props.projects).map((project) => ({
      ...project.fields,
      key: project.pk
    }))

    setAllProjects(projects)
  }, [setAllProjects])

  const showPotentialProject = (selectedProject) => {
    const project = allProjects.filter(project => project.key == selectedProject.value)
    setPotentialProject(project[0])
  }

  const addProjectToPortfolio = () => {
    // Make sure the project doesn't already exist before adding it to the portfolio.
    if (!portfolio.projects.includes(potentialProject)) {
      setPortfolio({projects: portfolio.projects.concat(potentialProject)})
    }

    // Reset the state so the DOM removes the AddPotentialProject component.
    setPotentialProject(null)
  }

  return (
  <>
    <div className="container">
      <div className="container row pt-5 mb-5 text-center">
        <h1>Build a 5-Year Plan</h1>
      </div>

      <div className="row w-100 mb-5">
        <SearchProjects 
          projects={allProjects} 
          onSelection={showPotentialProject} />
      </div>

      <div className="mb-5">
        {potentialProject && 
          <AddProjectToPlan 
            project={potentialProject} 
            addProjectOnClick={addProjectToPortfolio} />
          }
      </div>

      {portfolio.projects.length > 0 ? 
        <div className="w-100">
          <PortfolioTable portfolio={portfolio.projects} /> 
          <PortfolioTotals portfolio={portfolio.projects} />
        </div> : null
      }
    </div>
  </>
)}

ReactDOM.render(
  React.createElement(Dashboard, window.props),
  window.reactMount,
)