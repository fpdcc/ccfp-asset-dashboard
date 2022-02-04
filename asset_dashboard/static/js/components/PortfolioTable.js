import React, { useState } from 'react'
import ReactTable from './BaseTable'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import InputGroup from 'react-bootstrap/InputGroup'

const PortfolioTable = ({ portfolio, columns, onRemoveFromPortfolio, savePortfolioName, savePortfolio, createNewPortfolio }) => {
  const [edit, setEdit] = useState(false)

  const onRowClick = ({ original }) => {
    return {
      onClick: e => {
        onRemoveFromPortfolio(original)
      }
    }
  }

  const updatePortfolioName = (e) => {
    savePortfolioName(e).then(
      setEdit(false)
    ).catch(err => console.error(err))
  }

  const _createNewPortfolio = (e) => {
    createNewPortfolio(e).then(
      setEdit(true)
    ).catch(err => console.error(err))
  }

  return (
    <div className="mb-5 mt-5">
      <h3>
        Portfolio
      </h3>
      {!edit &&
        <h4>
          {portfolio.name}
          <div className="float-right">
            <Button
              variant="success"
              size="sm"
              type="button"
              id="edit-portfolio"
              className="mr-2"
              onClick={() => setEdit(true)}>
              Edit name
            </Button>
            <Button
              variant="secondary"
              size="sm"
              type="link"
              id="new-portfolio"
              onClick={_createNewPortfolio}>
              New portfolio
            </Button>
          </div>
        </h4>
      }
      {edit &&
        <Form id="portfolio-form" onSubmit={updatePortfolioName}>
          <InputGroup className="mb-3">
            <Form.Control
              placeholder="Enter a name for your portfolio..."
              defaultValue={portfolio.name ? portfolio.name : ''}
              aria-label="Portfolio name"
              required={true}
              className="mr-2"
              id="portfolio-name"
              name="portfolio-name"
            />
            <Button
              variant="primary"
              size="sm"
              type="submit"
              id="save-portfolio-name"
              className="mr-3">
              Save name
            </Button>
            <Button
              variant="link"
              size="sm"
              type="button"
              id="cancel-edit"
              onClick={() => setEdit(false)}>
              Cancel
            </Button>
          </InputGroup>
        </Form>
      }
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
      {portfolio.name &&
        <div className="d-flex justify-content-center">
          <Button
            variant={portfolio.unsavedChanges ? 'primary' : 'link'}
            type="button"
            id="save-portfolio-contents"
            disabled={portfolio.unsavedChanges ? false : true}
            className="mr-2 px-3"
            onClick={savePortfolio}>
            {portfolio.unsavedChanges
              ? 'Save portfolio'
              : 'All changes saved'
            }
          </Button>
        </div>
      }
    </div>
  )
}

export default PortfolioTable
