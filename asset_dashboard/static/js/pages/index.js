import React from 'react'
import ReactDOM from 'react-dom'
import ProjectsTable from './components/ProjectsTable'
import PortfolioTable from './components/PortfolioTable'
import PortfolioTotals from './components/PortfolioTotals'
import calculateTotals from './helpers/calculateTotals.js'
import SearchInput from './components/FilterComponent'

class PortfolioPlanner extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      allProjects: [],
      portfolio: {
        projects: [],
        totals: {
          budgetImpact: 0,
          projectNames: [],
          projectZones: []
        }
      },
      columns: [
        {
          name: 'Project Description',
          selector: 'projectDescription', 
          sortable: true,
          maxWidth: '550px'
        },
        {
          name: 'Total Score',
          selector: 'score',
          sortable: true,
          maxWidth: '50px',
        },
        {
          name: 'Total Budget',
          selector: 'budget',
          sortable: true,
          maxWidth: '75px'
        }
      ],
      filterText: '',
      filteredRows: []
    }

    this.updatePortfolio = this.updatePortfolio.bind(this)
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
        isDisabled: false
      }
    })

    this.setState({
      allProjects: projects,
      filteredRows: projects
    })
  }

  updatePortfolio(projectsInPortfolio) {
    const totals = calculateTotals(projectsInPortfolio)

    this.setState({
      portfolio: {
        projects: projectsInPortfolio,
        totals: totals
      }
    })
  }

  searchProjects(e) {
    const filterText = e.target.value
    const filteredRows = this.state.allProjects && this.state.allProjects.filter(project => {
      return project.projectDescription.toLowerCase().includes(filterText.toLowerCase())
    })

    this.setState({
      filterText: filterText,
      filteredRows: filteredRows
    })
  }

  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="container col card mt-5 col-9">
            <h1 className="pt-5 pl-3">Build a 5-Year Plan</h1>
            <div className="w-100">
              <SearchInput 
                onFilter={e => this.searchProjects(e)} 
                filterText={this.state.filterText} />
              <div className="table-responsive">
                <PortfolioTable 
                  portfolioProjects={this.state.portfolio.projects} 
                  columns={this.state.columns} />
                <ProjectsTable 
                  allProjects={this.state.filteredRows}
                  columns={this.state.columns}
                  onPortfolioChange={this.updatePortfolio} />
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