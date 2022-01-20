import React from 'react'
import ReactTable from './BaseTable'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import InputGroup from 'react-bootstrap/InputGroup'

const PortfolioTable = ({ portfolio, columns, onRemoveFromPortfolio, onNameChange, savePortfolio }) => {
  const onRowClick = ({ original }) => {
    return {
      onClick: e => {
        onRemoveFromPortfolio(original)
      }
    }
  }

  return (
    <div className="mb-5 mt-5">
      <h3>
        Portfolio
      </h3>
      <>
        <InputGroup className="mb-3">
          <Form.Control
            placeholder="Enter a name for your portfolio..."
            value={portfolio.name ? portfolio.name : ''}
            aria-label="Portfolio name"
            aria-describedby="portfolioName"
            onChange={onNameChange}
          />
          <Button
            variant="primary"
            type="submit"
            id="save-portfolio"
            onClick={savePortfolio}
            disabled={portfolio.unsavedChanges ? false : true}>
            Save portfolio
          </Button>
        </InputGroup>
      </>
      <ReactTable
        columns={columns}
        rows={portfolio.projects}
        getTrProps={onRowClick}
        rowClassNames='table-info'
        selector={() => {
          return (
            <span>
              <i className="fa fa-minus-square bg-"></i>
            </span>
          )
        }}
      />
    </div>
  )
}

export default PortfolioTable
