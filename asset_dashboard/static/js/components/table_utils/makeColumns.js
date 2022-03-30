export default function makeColumns(rows, columns) {
  if (rows[0]?.properties.grove_number) {
    const newColumns = [
      {
        Header: 'Grove',
        accessor: 'properties.grove_number', 
      },
      ...columns
    ]

    return newColumns
  } else if (rows[0]?.properties.complex) {
    const newColumns = [
      ...columns, 
      {
        Header: 'Complex',
        accessor: 'properties.complex', 
      }
    ]
    return newColumns
  } else {
    return columns
  }
}