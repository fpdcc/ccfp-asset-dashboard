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
      {!edit &&
        <h3>
          {portfolio.name}
          <Button
            variant="outline-success"
            type="button"
            id="edit-portfolio"
            className="ml-2"
            onClick={() => setEdit(true)}>
            Edit name
          </Button>
          {portfolio.name &&
            <div className="float-right">
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
              <Button
              variant="secondary"
                type="link"
                id="new-portfolio"
                onClick={_createNewPortfolio}>
                New portfolio
              </Button>
            </div>
          }
        </h3>
      }
      {edit &&
        <Form id="portfolio-form" onSubmit={updatePortfolioName}>
          <InputGroup className="mb-3">
            <Form.Control
              placeholder="Enter a name for your portfolio..."
              defaultValue={portfolio.name ? portfolio.name : ''}
              aria-label="Portfolio name"
              required={true}
              className="mr-2 form-control-lg"
              id="portfolio-name"
              name="portfolio-name"
            />
            <Button
              variant="primary"
              type="submit"
              id="save-portfolio-name"
              className="mr-3">
              Save name
            </Button>
            {portfolio.name &&
              <Button
                variant="link"
                type="button"
                id="cancel-edit"
                onClick={() => setEdit(false)}>
                Cancel
              </Button>
            }
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
    </div>
  )
}

export default PortfolioTable
