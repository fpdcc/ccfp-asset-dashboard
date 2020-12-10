const calculateTotals = (portfolio) => {
return {
    budgetImpact: portfolio.reduce((total, project) => { return total + project.budget }, 0),
    projectNames: portfolio.map(project => project.name),
    projectZones: portfolio.map(project => project.zone)
    }
}

export default calculateTotals