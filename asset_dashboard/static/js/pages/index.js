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

  const calculateTotals = (portfolio) => {
    return {
      budgetImpact: portfolio.reduce((total, project) => { return total + project.budget }, 0),
      projectNames: portfolio.map(project => project.name),
      projectZones: portfolio.map(project => project.zone)
    }
  }

  const addProjectToPortfolio = () => {
    // Make sure the project doesn't already exist before adding it to the portfolio.
    if (!portfolio.projects.includes(potentialProject)) {
      // Update the portfolio array with the new project.
      const updatedPortfolio =  portfolio.projects.concat(potentialProject)

      // Re-calculate the totals based on the updatedPortfolio.
      const updatedTotals = calculateTotals(updatedPortfolio)

      setPortfolio({
        projects: updatedPortfolio, 
        totals: updatedTotals
      })
    }

    // Reset the state so the AddPotentialProject component is removed from the DOM.
    setPotentialProject(null)
  }

  const removeProjectFromPortfolio = (key) => {
    // Filter the project out of the portfolios.
    const updatedPortfolio = portfolio.projects.filter((project) => {
      if (project.key !== key) {
        return project
      }
    })

    // Re-calculate the totals.
    const updatedTotals = calculateTotals(updatedPortfolio)

    // Reset state so the table and totals rerender.
    setPortfolio({
      projects: updatedPortfolio, 
      totals: updatedTotals
    })
  }

  function onRowClick({ original }) {
    return {
      onClick: e => {
        e.preventDefault()
        removeProjectFromPortfolio(original.key)
      }
    }
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
          <PortfolioTable portfolio={portfolio.projects} getTrProps={onRowClick} /> 
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