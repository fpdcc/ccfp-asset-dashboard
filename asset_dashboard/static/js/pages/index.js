import React, { useState, useEffect } from 'react'
import ReactDOM from 'react-dom'
import SearchProjects from './SearchProjects'
import PortfolioTable from './PortfolioTable'
import PortfolioTotals from './PortfolioTotals'
import AddProjectToPlan from './AddProjectToPlan'

const PortfolioPlanner = (props) => {  
  const [allProjects, setAllProjects] = useState([])
  const [potentialProject, setPotentialProject] = useState(null)
  const [portfolio, setPortfolio] = useState({projects: [], totals: {}})

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
    const project = allProjects.filter(project => project.key == selectedProject.value)[0]
    setPotentialProject(project)
  }

  const addProjectToPortfolio = () => {
    // Make sure the project doesn't already exist before adding it to the portfolio.
    if (!portfolio.projects.includes(potentialProject)) {
      // Update the portfolio array with the new project.
      const updatedPortfolio =  portfolio.projects.concat(potentialProject)

      // Re-calculate the totals based on the updatedPortfolio.
      const updatedTotals = {
        budgetImpact: updatedPortfolio.reduce((total, project) => { return total + project.budget }, 0),
        projectNames: updatedPortfolio.map(project => project.name),
        projectZones: updatedPortfolio.map(project => project.zone)
      }

      setPortfolio({projects: updatedPortfolio, totals: updatedTotals})
    }

    // Reset the state so the AddPotentialProject component is removed from the DOM.
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
          <PortfolioTotals totals={portfolio.totals} />
        </div> : null
      }
    </div>
  </>
)}

ReactDOM.render(
  React.createElement(PortfolioPlanner, window.props),
  window.reactMount,
)