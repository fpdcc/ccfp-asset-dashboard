import React, { useState, useEffect } from 'react'
import ReactTable from './BaseTable'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import InputGroup from 'react-bootstrap/InputGroup'
import projectColumns from './table_utils/projectColumns'
import SubRow from './table_utils/SubRow'
import PortfolioPicker from './PortfolioPicker'

export const PortfolioTable = ({ rows, onRemoveFromPortfolio  }) => {
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
    <div>
      <ReactTable
        columns={React.useMemo(() => projectColumns(Selector, onRemoveFromPortfolio), [])}
        rows={rows}
        renderRowSubComponent={React.useCallback(SubRow, [])}
      />
    </div>
  )
}


export function PortfolioControl({ portfolio, savePortfolioName, savePortfolio, createNewPortfolio, changePortfolio, portfolios }) {
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

  return (
    <>
      {!edit &&
        <>
          {portfolio.name &&
            <div className="col d-flex flex-column justify-content-center align-items-start">
              <div className='row align-items-center'>
                <h1>{portfolio.name}</h1>
                <div>
                  <Button
                    variant="outline-success"
                    size="sm"
                    type="button"
                    id="edit-portfolio"
                    className="ml-2"
                    onClick={() => setEdit(true)}>
                    Edit name
                  </Button>
                </div>
              </div>
              <div className='row'>
                {portfolio.unsavedChanges
                  ? (
                    <Button
                      variant='primary'
                      size="lg"
                      type="button"
                      id="save-portfolio-contents"
                      disabled={portfolio.unsavedChanges ? false : true}
                      className="mr-2 px-3"
                      onClick={savePortfolio}>
                      Save portfolio
                    </Button>
                  )
                  : (<p className="text-secondary">All changes saved</p>)
                }
              </div>
            </div>
          }

         <div className="col-4 d-flex align-items-center h2">
            <PortfolioPicker
              portfolios={portfolios}
              activePortfolio={portfolio}
              changePortfolio={changePortfolio}
            />
            <div className="d-flex align-items-end h-100">
              <Button
                variant="secondary"
                type="link"
                id="new-portfolio"
                onClick={_createNewPortfolio}>
                New portfolio
              </Button>
            </div>
         </div>
        </>
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
    </>
  )
}
