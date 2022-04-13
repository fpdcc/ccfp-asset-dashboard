import React from 'react'
import PortfolioTotalsTable from './tables/PortfolioTotalsTable'

const PortfolioTotals = ({ totals }) => {
    return (
      <div className="mt-5">
        <div className="mt-2 col card shadow-sm pt-2 text-center">
          <h5>Budget Impact</h5>
          <h3>${totals.budgetImpact.toLocaleString() || 0}</h3>
        </div>

        {
          totals.totalEstimatedCostByYear && 
          <div className="mt-2 col card shadow-sm pt-2 text-center">
            <h5>Total Estimated Cost by Fiscal Year</h5>
            <PortfolioTotalsTable totals={totals.totalEstimatedCostByYear} />
          </div>
        }
        
        {
          totals.totalFundedAmountByYear &&
            <div className="mt-2 col card shadow-sm pt-2 text-center">
              <h5>Total Funded Amount by Fiscal Year</h5>
              <ul className="list-unstyled">
                <PortfolioTotalsTable totals={totals.totalFundedAmountByYear} />
              </ul>
            </div>
        }
        
        {
          totals.totalEstimatedCostByZone &&
            <div className="mt-2 col card shadow-sm pt-2 text-center">
              <h5>Total Cost by Zone by Fiscal Year</h5>
              <p>todo</p>
            </div>
        }
      </div>
    )
  }

export default PortfolioTotals
