import React from 'react'
import ReactDOM from 'react-dom'
import Button from 'react-bootstrap/Button'
import { CSVLink } from 'react-csv'
import Cookies from 'js-cookie'

import ProjectsTable from './components/ProjectsTable'
import PortfolioTable from './components/PortfolioTable'
import PortfolioTotals from './components/PortfolioTotals'
import PortfolioPicker from './components/PortfolioPicker'
import SectionPicker from './components/SectionPicker'
import SearchInput from './components/SearchInput'

class PortfolioPlanner extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      allProjects: [],
      remainingProjects: [],
      allPortfolios: [],
      sections: [],
      portfolio: {
        id: null,
        name: '',
        projects: [],
        totals: {
          budgetImpact: 0,
          projectNames: [],
          projectZones: []
        },
        unsavedChanges: false
      },
      filterText: '',
      selectedSection: ''
    }

    this.searchProjects = this.searchProjects.bind(this)
    this.addProjectToPortfolio = this.addProjectToPortfolio.bind(this)
    this.removeProjectFromPortfolio = this.removeProjectFromPortfolio.bind(this)

    this.selectPortfolio = this.selectPortfolio.bind(this)
    this.createNewPortfolio = this.createNewPortfolio.bind(this)
    this.savePortfolio = this.savePortfolio.bind(this)
    this.savePortfolioName = this.savePortfolioName.bind(this)

    this.alertUser = this.alertUser.bind(this)
    this.confirmDestroy = this.confirmDestroy.bind(this)
    this.changeSection = this.changeSection.bind(this)
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
        zones: project.zones || 'N/A',
        cost_by_zone: project.cost_by_zone,
        house_districts: project.house_districts,
        senate_districts: project.senate_districts,
        commissioner_districts: project.commissioner_districts,
        key: project.pk,
        funding_streams: project.funding_streams,
        total_estimated_cost: parseFloat(project.total_estimated_cost),
        year: project.year,
        estimated_bid_quarter: project.estimated_bid_quarter,
        status: project.status,
        project_manager: project.project_manager,
        countywide: project.countywide,
      }
    })

    let state = {
      allProjects: projects,
      remainingProjects: projects,
      allPortfolios: props.portfolios,
      sections: [...new Set(projects.map(project => { return project.section }))]
    }

    // Rehydate state from last edited portfolio, if one exists
    if (props.selectedPortfolio) {
      const [portfolioObj, remainingProjects] = this.hydratePortfolio(
        props.selectedPortfolio,
        projects
      )

      state = {
        ...state,
        remainingProjects: remainingProjects,
        portfolio: portfolioObj
      }
    }

    this.setState(state)

    window.addEventListener('beforeunload', this.alertUser)
  }

  componentWillUnmount() {
    window.removeEventListener('beforeunload', this.alertUser)
  }

  // Project methods
  searchProjects(e) {
    const filterText = e.target.value

    this.setState({
      filterText: filterText
    })
  }
  
  filterBySection(projects){ 
    const filteredProjects = projects.filter(project => {
      if (this.state.selectedSection !== '') {
        return project.section.toLowerCase().includes(this.state.selectedSection.toLowerCase())
      } else {
        return project
      }
    })
  }

  addProjectToPortfolio(row) {
    // add the row to the existing portfolio
    const updatedProjectsInPortfolio = [...this.state.portfolio.projects, row]

    const updatedTotals = this.calculateTotals(updatedProjectsInPortfolio)

    // remove the row from the remaining projects
    const updatedRemainingProjects = this.state.remainingProjects.filter((project) => {
      if (project.key !== row.key) {
        return project
      }
    })

    this.setState({
      portfolio: {
        ...this.state.portfolio,
        projects: updatedProjectsInPortfolio,
        totals: updatedTotals
      },
      remainingProjects: updatedRemainingProjects
    })

    this.registerPortfolioChange()
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
        ...this.state.portfolio,
        projects: updatedPortfolio,
        totals: this.calculateTotals(updatedPortfolio)
      },
      remainingProjects: remainingProjects
    })

    this.registerPortfolioChange()
  }

  // Portfolio methods
  selectPortfolio(e) {
    if (this.state.portfolio.unsavedChanges && !this.confirmDestroy()) {
      return
    }

    const selectedPortfolio = this.state.allPortfolios.find(
      portfolio => portfolio.id == e.target.value
    )

    const [portfolioObj, remainingProjects] = this.hydratePortfolio(
      selectedPortfolio,
      this.state.allProjects
    )

    this.setState({
      remainingProjects: remainingProjects,
      portfolio: portfolioObj
    })
  }

  createNewPortfolio(e) {
    return new Promise((resolve, reject) => {
      if (this.state.portfolio.unsavedChanges && !this.confirmDestroy()) {
        reject('Could not create new portfolio')
        return
      }

      this.setState({
        portfolio: {
          id: null,
          name: '',
          projects: [],
          totals: {
            budgetImpact: 0,
            projectNames: [],
            projectZones: []
          },
          unsavedChanges: false
        },
        remainingProjects: this.state.allProjects
      })

      resolve()
    })
  }

  savePortfolio(e) {
    e.preventDefault()

    const data = {
      name: this.state.portfolio.name,
      user: props.userId,
      phases: this.state.portfolio.projects.map((phase, index) => {
        return {'phase': phase.key, 'sequence': index + 1}
      })
    }

    const [url, method] = this.state.portfolio.id
      ? [`/portfolios/${this.state.portfolio.id}/`, 'PATCH'] // Update
      : ['/portfolios/', 'POST'] // Create

    fetch(url, {
      method: method,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFTOKEN': Cookies.get('csrftoken')
      },
      body: JSON.stringify(data)
    }).then(response => {
      return response.json()
    }).then(portfolioObj => {
      let state = {
        portfolio: {
          ...this.state.portfolio,
          id: portfolioObj.id,
          unsavedChanges: false
        }
      }

      if (method == 'POST') {
        // Add newly created portfolio to the portfolio array
        this.setState({
          ...state,
          allPortfolios: [...this.state.allPortfolios, portfolioObj]
        })
      } else {
        // Update existing portfolio in the portfolio array
        this.setState({
          ...state,
          allPortfolios: this.state.allPortfolios.map(portfolio => {
            return portfolio.id === portfolioObj.id ? portfolioObj : portfolio
          })
        })
      }
    }).catch(error => {
      console.error(error)
    })
  }

  savePortfolioName(e) {
    e.persist()

    return new Promise((resolve, reject) => {
      const portfolioName = new FormData(e.target).get('portfolio-name')

      try {
        this.setState({
          portfolio: {...this.state.portfolio, name: portfolioName}
        }, () => this.savePortfolio(e))
      } catch (err) {
        reject(err)
        return
      }

      resolve()
    })
  }

  // Methods to alert user of unsaved changes on navigation
  alertUser(e) {
    if (this.state.portfolio.unsavedChanges) {
      e.preventDefault()
      e.returnValue = ''
    }
  }

  confirmDestroy(e) {
   if (this.state.portfolio.unsavedChanges) {
      return confirm('The current portfolio has unsaved changes. Are you ' +
        'sure you want to switch portfolios? Changes you made may not be saved.')

      if (!confirmDestroy) {
        reject('Could not create new portfolio')
        return
      }
    }
  }

  // Helper methods
  calculateTotals(portfolio) {
    return {
      budgetImpact: portfolio.reduce((total, project) => { return total + project.budget }, 0),
      totalEstimatedCostByYear: this.calculateEstimatedCostByKey(portfolio, 'year', 'total_estimated_cost'),
      totalFundedAmountByYear: this.calculateFundedAmountByYear(portfolio),
      totalEstimatedZoneCostByYear: this.calculateZoneCostByYear(portfolio)
    }
  }
  
  calculateEstimatedCostByKey(rows, accumulatorKey, addendField) {
    let results = {}
    
    rows.forEach(project => {
      const key = project[accumulatorKey] ? project[accumulatorKey] : 'N/A' // test data has no key value...
      
      let total = results[key] ? results[key] : 0
      
      results = {
        ...results,
        [key]: total += parseFloat(project[addendField])
      }

    })

    return results
  }
  
  calculateFundedAmountByYear(portfolio) {
    let results = {}

    portfolio.forEach(project => {
      const fundingByYear = this.calculateEstimatedCostByKey(project.funding_streams, 'year', 'budget')

      for (const [key, value] of Object.entries(fundingByYear)) {
        let yearTotal = results[key] ? results[key] : 0
        results = {
          ...results,
          [key]: yearTotal += value
        }
      }
    })

    return results
  }
  
  calculateZoneCostByYear(portfolio) {
    let yearTotals = {}

    portfolio.forEach(phase => {
      const year = phase['year']

      if (!yearTotals[year] && year !== null) {
        yearTotals[year] = {}
      }
      
      for (const [key, value] of Object.entries(phase.cost_by_zone)) {
        let total = yearTotals[year][key] ? yearTotals[year][key] : 0

        yearTotals[year] = {
          ...yearTotals[year],
          [key]: total += value
        }
      }
    })

    return yearTotals
  }

  hydratePortfolio(portfolio, projects) {
    const selectedProjectIds = portfolio.phases.map(phase => phase.phase)

    const portfolioProjects = projects.filter(
      project => selectedProjectIds.includes(project.key)
    )

    const remainingProjects = projects.filter(
      project => !selectedProjectIds.includes(project.key)
    )

    const portfolioObj = {
      id: portfolio.id,
      name: portfolio.name,
      projects: portfolioProjects,
      totals: this.calculateTotals(portfolioProjects),
      unsavedChanges: false
    }

    return [ portfolioObj, remainingProjects ]
  }

  registerPortfolioChange(e) {
    // Register unsaved changes to a portfolio after a state change
    this.setState((state, props) => ({
      portfolio: {...state.portfolio, unsavedChanges: true}
    }))
  }

  getDate() {
    const date = new Date(new Date().toString().split('GMT')[0]+' UTC').toISOString().split('T')[0]
    return date
  }
  
  changeSection(e) {
    const newSection = e.target.value
    this.setState(prevState => {
      return {
        ...prevState,
        selectedSection: newSection
      }
    })
  }

  render() {
    // This filters on every re-render, so that this.state.remainingProjects can be the source of truth.
    // Could also chain filtering here for other things (like "department" from the wireframe).
    const filteredRows = this.state.remainingProjects && this.state.remainingProjects.filter(project => {
      return project.description.toLowerCase().includes(this.state.filterText.toLowerCase())
    }).filter(project => {
      if (this.state.selectedSection !== '') {
        return project.section.toLowerCase().includes(this.state.selectedSection.toLowerCase())
      } else {
        return project
      }
    })
    
    const filteredPortfolio = this.state.portfolio.projects && this.state.portfolio.projects.filter(project => {
      return project
    }).filter(project => {
      if (this.state.selectedSection !== '') {
        return project.section.toLowerCase().includes(this.state.selectedSection.toLowerCase())
      } else {
        return project
      }
    })

    return (
      <div className="m-5">
        <div className="row">
          <div className="col">
            <h1>Build a 5-Year Plan</h1>
          </div>
          <div className="row col">
            <PortfolioPicker
              portfolios={this.state.allPortfolios}
              activePortfolio={this.state.portfolio}
              changePortfolio={this.selectPortfolio}
            />
            <SectionPicker 
              sections={this.state.sections}
              activeSection={this.state.selectedSection}
              changeSection={this.changeSection}
            />
          </div>
        </div>
        <div className="row">
          <div className="container col card shadow-sm mt-5 ml-3 col-9">
              <>
                <PortfolioTable
                  portfolio={this.state.portfolio}
                  rows={filteredPortfolio}
                  onRemoveFromPortfolio={this.removeProjectFromPortfolio}
                  savePortfolio={this.savePortfolio}
                  savePortfolioName={this.savePortfolioName}
                  createNewPortfolio={this.createNewPortfolio} />
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
                    className='btn btn-info mx-auto'
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
