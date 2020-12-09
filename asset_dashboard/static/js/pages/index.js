import React, { useState, useEffect } from 'react'
import ReactDOM from 'react-dom'
import PortfolioTable from './PortfolioTable'
import PortfolioTotals from './PortfolioTotals'

const inititalPortfolio = {
  projects: [],
  totals: {
    budgetImpact: 0,
    projectNames: [],
    projectZones: []
  }
}

const PortfolioPlanner = (props) => {  
  const [allProjects, setAllProjects] = useState([])
  const [portfolio, setPortfolio] = useState(inititalPortfolio)
  const [remainingProjects, setRemainingProjects] = useState([])

  useEffect(() => {
    const projects = JSON.parse(props.projects).map((project) => ({
      ...project.fields,
      key: project.pk
    }))

    setAllProjects(projects)
    setRemainingProjects(projects)
  }, [setAllProjects, setRemainingProjects])

  const calculateTotals = (portfolio) => {
    return {
      budgetImpact: portfolio.reduce((total, project) => { return total + project.budget }, 0),
      projectNames: portfolio.map(project => project.name),
      projectZones: portfolio.map(project => project.zone)
    }
  }

  // This function handles the big, "all projects" table.
  // It executes anytime a row is selected or deselected.
  // This is the only thing I need to calculate the portfolio.
  const updatePortfolio = (projectsToAdd) => {
    // filter out the projects from the remainingProjects state
    // so the remainingProjects can update the main table
    const updatedRemainingProjects = remainingProjects.filter((existingProject) => {
      if (!projectsToAdd.includes(existingProject)) {
        return existingProject
      }
    })

    const totals = calculateTotals(projectsToAdd)

    setRemainingProjects(updatedRemainingProjects)
    setPortfolio({
      projects: projectsToAdd, 
      totals: totals
    })
  }

  // This manages the row selection for the "portfolio" table.
  // It's doing almost the exact same as the updatePortfolio function,
  // except I'm filtering different arrays and setting different elements of state.
  // I have to update the other table and keep it in sync with this table.
  // This is where it gets tricky and buggy. How do I update the state based on what's passed from this table?
  // How do I keep it in sync with the portfolio calculator and the remainingProjects table?
  // Currently, his works for one click and then the state gets all messed up.
  // Also, i'm not sure how to make it appear "checked", and how to programmatically deselect the "checked" state 
  // for this row in the other table
  const removeProjectFromPortfolio = (projectToRemove) => {
    const updatedPortfolioProjects = portfolio.projects.filter((project) => {
      if (project.key !== projectToRemove.key) {
        return project
      }
    })

    const updatedTotals = calculateTotals(updatedPortfolioProjects)

    setPortfolio({
      projects: updatedPortfolioProjects,
      totals: updatedTotals
    })

    setRemainingProjects([...remainingProjects, projectToRemove])
  }

  return (
  <div className="container">
    <div className="row">
      <div className="container col card mt-5 col-9">
        <h1 className="pt-5 pl-3">Build a 5-Year Plan</h1>
        <div className="w-100">
          <PortfolioTable 
            portfolio={portfolio.projects}
            projects={remainingProjects} 
            onUpdatePortfolio={updatePortfolio}
            onRemoveProject={removeProjectFromPortfolio} />
        </div>
      </div>
      <div className="col">
        <PortfolioTotals totals={portfolio.totals} />
      </div>
    </div>
  </div>
)}

ReactDOM.render(
  React.createElement(PortfolioPlanner, window.props),
  window.reactMount,
)