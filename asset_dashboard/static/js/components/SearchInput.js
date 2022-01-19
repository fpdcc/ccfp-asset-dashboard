import React from 'react'
import styled from 'styled-components'
import PropTypes from 'prop-types'

const TextField = styled.input`
  border-radius: 3px;
  border-top-left-radius: 5px;
  border-bottom-left-radius: 5px;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  border: 1px solid #e5e5e5;
  padding: 0 32px 0 16px;
`;

const SearchInput = ({ filterText, onFilter, placeholder, ariaLabel }) => {
  return (
    // TODO: better styling so we can reuse it. changing it in one place will break in another..
    <div className="mb-4 col-12">
      <TextField 
        id="search" 
        type="text" 
        placeholder={placeholder} 
        aria-label={ariaLabel}
        value={filterText} 
        onChange={onFilter} />
    </div>
  )
}

SearchInput.propTypes = {
  filterText: PropTypes.string,
  onFilter: PropTypes.func.isRequired
}

export default SearchInput
