import React from 'react'
import ReactDOM from 'react-dom'
import ProjectsTable from './components/ProjectsTable'
import PortfolioTable from './components/PortfolioTable'
import PortfolioTotals from './components/PortfolioTotals'
import SearchInput from './components/FilterComponent'

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
      },
      filterText: ''
    },

    this.columns = [
      {
        Header: 'Project Description',
        accessor: 'projectDescription', 
      },
      {
        Header: 'Total Score',
        accessor: 'score',
      },
      {
        Header: 'Total Budget',
        accessor: 'budget',
      }
    ],

    this.addProjectToPortfolio = this.addProjectToPortfolio.bind(this)
    this.removeProjectFromPortfolio = this.removeProjectFromPortfolio.bind(this)
    this.searchProjects = this.searchProjects.bind(this)
  }

  componentDidMount() {
    const projects = JSON.parse(props.projects).map((project) => {
      return {
        key: project.pk,
        projectDescription: project.fields.project_description || 'No description available.',
        score: project.fields.score || 'N/A',
        budget: project.fields.budget || 0,
        name: project.fields.name,
        zone: project.fields.zone,
      }
    })

    this.setState({
      allProjects: projects,
      remainingProjects: projects
    })
  }

  calculateTotals(portfolio) {
    return {
      budgetImpact: portfolio.reduce((total, project) => { return total + project.budget }, 0),
      projectNames: portfolio.map(project => project.name),
      projectZones: portfolio.map(project => project.zone)
    }
  }

  addProjectToPortfolio(row) {
    // add the row to the existing portfolio
    const updatedProjectsInPortfolio = [...this.state.portfolio.projects, row]

    const updatedTotals =this.calculateTotals(updatedProjectsInPortfolio)

    // remove the row from the remaining projects
    const updatedRemainingProjects = this.state.remainingProjects.filter((project) => {
      if (project.key !== row.key) {
        return project
      }
    })

    this.setState({
      portfolio: {
        projects: updatedProjectsInPortfolio,
        totals: updatedTotals
      },
      remainingProjects: updatedRemainingProjects
    })
  }

  removeProjectFromPortfolio(row) {
    // remove the row from the existing portfolio
    const updatedPortfolio = this.state.portfolio.projects.filter((project) => {
      if (project.key != row.key) {
        return project
      }
    })

    // add the project back to the remainingProjects
    this.setState(prevState => ({
      portfolio: {
        projects: updatedPortfolio,
        totals: this.calculateTotals(updatedPortfolio)
      },
      remainingProjects: [...prevState.remainingProjects, row]
    }))
  }

  searchProjects(e) {
    const filterText = e.target.value

    this.setState({
      filterText: filterText
    })
  }

  render() {
    // This filters on every re-render, so that this.state.remainingProjects can be the source of truth.
    // Could also chain filtering here for other things (like "department" from the wireframe).
    const filteredRows = this.state.remainingProjects && this.state.remainingProjects.filter(project => {
      return project.projectDescription.toLowerCase().includes(this.state.filterText.toLowerCase())
    })

    return (
      <div className="container">
        <div className="row">
          <div className="container col card mt-5 col-9">
            <h1 className="pt-5 pl-3">Build a 5-Year Plan</h1>
            <div className="w-100">
              <SearchInput
                onFilter={this.searchProjects} 
                filterText={this.state.filterText} />
              <div className="table-responsive">
                <PortfolioTable 
                  portfolioProjects={this.state.portfolio.projects} 
                  columns={this.columns} 
                  onRemoveFromPortfolio={this.removeProjectFromPortfolio} />
                <ProjectsTable 
                  allProjects={filteredRows}
                  columns={this.columns}
                  onAddToPortfolio={this.addProjectToPortfolio} />
              </div>
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