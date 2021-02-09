import React from 'react'
import ReactDOM from 'react-dom'
import ProjectsTable from './components/ProjectsTable'
import PortfolioTable from './components/PortfolioTable'
import PortfolioTotals from './components/PortfolioTotals'
import SearchInput from './components/FilterComponent'
import { CSVLink } from 'react-csv'

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
    }

    this.addProjectToPortfolio = this.addProjectToPortfolio.bind(this)
    this.removeProjectFromPortfolio = this.removeProjectFromPortfolio.bind(this)
    this.searchProjects = this.searchProjects.bind(this)
  }

  createRegionName(regions) {
    // returns a CSV string of names for the different regions
    const names = regions.map(({ name }) => {
      return name
    }).join(',')

    return names
  }

  componentDidMount() {
    // prepare the data so it can be used in the table and exported as CSV
    const projects = JSON.parse(props.projects).map((project) => {
      return {
        name: project.name,
        description: project.description || 'No description available.',
        section: project.section,
        category: project.category,
        budget: parseFloat(project.total_budget) || 0,
        score: project.total_score || 'N/A',
        phase: project.phase || 'N/A',
        zones: this.createRegionName(project.zones) || 'N/A',
        house_districts: this.createRegionName(project.house_districts),
        senate_districts: this.createRegionName(project.senate_districts),
        commissioner_districts: this.createRegionName(project.commissioner_districts),
        key: project.pk
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
      projectZones: portfolio.map(project => project.zones.split(','))
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

    // reset the list of remainingProjects, based on the updated portfolio
    const remainingProjects = this.state.allProjects.filter(project => {
      if (!updatedPortfolio.includes(project)) {
        return project
      }
    })

    this.setState({
      portfolio: {
        projects: updatedPortfolio,
        totals: this.calculateTotals(updatedPortfolio)
      },
      remainingProjects: remainingProjects
    })
  }

  searchProjects(e) {
    const filterText = e.target.value

    this.setState({
      filterText: filterText
    })
  }

  getDate() {
    const date = new Date(new Date().toString().split('GMT')[0]+' UTC').toISOString().split('T')[0]
    return date
  }

  render() {
    // This filters on every re-render, so that this.state.remainingProjects can be the source of truth.
    // Could also chain filtering here for other things (like "department" from the wireframe).
    const filteredRows = this.state.remainingProjects && this.state.remainingProjects.filter(project => {
      return project.description.toLowerCase().includes(this.state.filterText.toLowerCase())
    })

    return (
      <div className="m-5">
        <h1>Build a 5-Year Plan</h1>
        <div className="row">
          <div className="container col card shadow-sm mt-5 ml-3 col-9">
              <>
                <PortfolioTable 
                  portfolioProjects={this.state.portfolio.projects} 
                  onRemoveFromPortfolio={this.removeProjectFromPortfolio} />
                <ProjectsTable 
                  allProjects={filteredRows}
                  onAddToPortfolio={this.addProjectToPortfolio}
                  searchInput={<SearchInput
                    onFilter={this.searchProjects} 
                    filterText={this.state.filterText} />} />
              </>
          </div>
          <div className="col">
            <PortfolioTotals totals={this.state.portfolio.totals} />
            { this.state.portfolio.projects.length > 0 
             ? <div className="d-flex justify-content-center mt-3">
                  <CSVLink 
                    data={this.state.portfolio.projects}
                    filename={`CIP-${this.getDate()}`}
                    className='btn btn-primary mx-auto'
                    >
                      Export as CSV
                  </CSVLink>
                </div> 
            : null }
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
