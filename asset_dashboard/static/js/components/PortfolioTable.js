import React, { useState, useEffect } from 'react'
import ReactTable from './BaseTable'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import InputGroup from 'react-bootstrap/InputGroup'
import projectColumns from './table_utils/projectColumns'
import SubRow from './table_utils/SubRow'

const PortfolioTable = ({ portfolio, rows, onRemoveFromPortfolio, savePortfolioName, savePortfolio, createNewPortfolio }) => {
  const [edit, setEdit] = useState(false)
  
  useEffect(() => {
    setEdit(portfolio.id == null ? true : false)
  }, [portfolio])

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

  const Selector = (row) => {
    return (
      <button 
        class='btn'
        type='button'
        onClick={() => onRemoveFromPortfolio(row)} 
        aria-label='Remove project from portfolio'>
          <i className="fa fa-minus-square fa-lg"></i>
      </button>
    )
  }

  return (
    <div className="mb-5 mt-5">
      {!edit &&
        <h3>
          {portfolio.name}
          <Button
            variant="outline-success"
            size="sm"
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
                size="sm"
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
                size="sm"
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
              Save
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
        columns={React.useMemo(() => projectColumns(Selector, onRemoveFromPortfolio), [])}
        rows={rows}
        renderRowSubComponent={React.useCallback(SubRow, [])}
      />
    </div>
  )
}

export default PortfolioTable
