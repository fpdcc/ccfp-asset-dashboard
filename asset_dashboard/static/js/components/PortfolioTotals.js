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
            <PortfolioTotalsTable totals={totals.totalEstimatedCostByYear} headers={['Year', 'Amount']} />
          </div>
        }
        
        {
          totals.totalFundedAmountByYear &&
            <div className="mt-2 col card shadow-sm pt-2 text-center">
              <h5>Total Funded Amount by Fiscal Year</h5>
              <PortfolioTotalsTable 
                totals={totals.totalFundedAmountByYear} 
                headers={['Year', 'Amount']}
                />
            </div>
        }
        
        {
          totals.totalEstimatedZoneCostByYear &&
            <div className="mt-2 col card shadow-sm pt-2 text-center">
              <h5>Total Cost by Zone by Fiscal Year</h5>
              {
                Object.entries(totals.totalEstimatedZoneCostByYear).map(total => {
                  return (
                    <div className='mt-3'>
                      <h6>{total[0]}</h6>
                      <PortfolioTotalsTable 
                        totals={total[1]} 
                        headers={['Zone', 'Amount']}
                        />
                    </div>
                  )
                })
              }
            </div>
        }
      </div>
    )
  }

export default PortfolioTotals
