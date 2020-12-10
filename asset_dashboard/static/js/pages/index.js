import React from 'react'
import ReactDOM from 'react-dom'
import PortfolioTable from './PortfolioTable'
import PortfolioTotals from './PortfolioTotals'
import calculateTotals from './helpers/calculateTotals.js'


class PortfolioPlanner extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      allProjects: [],
      remainingProjects: [],
      portfolio: {
        projects: [],
        totals: {
          budgetImpact: 0,
          projectNames: [],
          projectZones: []
        }
      }
    }
  }

  componentDidMount() {
    const projects = JSON.parse(props.projects).map((project) => ({
      ...project.fields,
      key: project.pk
    }))

    this.setState({
      allProjects: projects,
      remainingProjects: projects
    })
  }

  addToPortfolio = (projectsToAdd) => {
    const updatedRemainingProjects = this.state.remainingProjects.filter((existingProject) => {
      if (!projectsToAdd.includes(existingProject)) {
        return existingProject
      }
    })

    const totals = calculateTotals(projectsToAdd)

    this.setState({
      remainingProjects: updatedRemainingProjects,
      portfolio: {
        projects: projectsToAdd,
        totals: totals
      }
    })
  }

  removeProjectFromPortfolio = (projectsToRemove) => {
    console.log('removeProjectFromPortfolio', projectsToRemove)
    
    // remove the projects from the portfolio
    const updatedPortfolioProjects = this.state.portfolio.projects.filter((project) => {
      if (!projectsToRemove.includes(project)) {
        return project
      }
    })

    // recalculate portfolio total
    const updatedTotals = calculateTotals(updatedPortfolioProjects)

    this.setState({
      portfolio: {
        projects: updatedPortfolioProjects,
        totals: updatedTotals
      },
      remainingProjects: [...this.state.remainingProjects, projectsToRemove]
    })
  }

  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="container col card mt-5 col-9">
            <h1 className="pt-5 pl-3">Build a 5-Year Plan</h1>
            <div className="w-100">
              <PortfolioTable 
                portfolio={this.state.portfolio.projects}
                projects={this.state.remainingProjects} 
                onAddToPortfolio={this.addToPortfolio}
                onRemoveProject={this.removeProjectFromPortfolio}
                 />
            </div>
          </div>
          <div className="col">
            <PortfolioTotals totals={this.state.portfolio.totals} />
          </div>
        </div>
      </div>
    )
  }
}

ReactDOM.render(
  React.createElement(PortfolioPlanner, window.props),
  window.reactMount,
)