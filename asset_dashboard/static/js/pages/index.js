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

  useEffect(() => {
    // Parse the props JSON string into an array of objects, 
    // then map each object to a new array.
    const projects = JSON.parse(props.projects).map((project) => ({
      ...project.fields,
      key: project.pk
    }))

    setAllProjects(projects)
  }, [setAllProjects])

  const calculateTotals = (portfolio) => {
    return {
      budgetImpact: portfolio.reduce((total, project) => { return total + project.budget }, 0),
      projectNames: portfolio.map(project => project.name),
      projectZones: portfolio.map(project => project.zone)
    }
  }

  const updatePortfolio = (projects) => {
    const totals = calculateTotals(projects)

    setPortfolio({
      projects: projects, 
      totals: totals
    })
  }

  return (
  <div className="container">
    <div className="row">
      <div className="container col card mt-5 col-9">
          <h1 className="pt-5 pl-3">Build a 5-Year Plan</h1>
        <div className="w-100">
          <PortfolioTable 
            portfolio={portfolio}
            projects={allProjects} 
            onUpdatePortfolio={updatePortfolio} />
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