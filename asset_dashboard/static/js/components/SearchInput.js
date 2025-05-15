import React from 'react'
import styled from 'styled-components';

const TextField = styled.input`
  height: 32px;
  width: 400px;
  border-radius: 3px;
  border-top-left-radius: 5px;
  border-bottom-left-radius: 5px;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  border: 1px solid #e5e5e5;
  padding: 0 32px 0 16px;

  &:hover {
    cursor: pointer;
  }
`;

const SearchInput = ({ filterText, onFilter }) => {
  return (
    <div className="input-group col-6">
      <input
        id="search"
        type="text"
        className='form-control'
        placeholder="Search for projects by name or ID"
        aria-label="Search Input"
        value={filterText}
        onChange={onFilter} />
    </div>
  )
}

export default SearchInput
