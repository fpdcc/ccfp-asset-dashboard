import React from 'react'

export default function Message({ text, messageTag, onCloseMessage }) {
  return (
    <div className={`alert alert-${messageTag}`} role="alert">
      <button 
          onClick={() => onCloseMessage(null)}
          type="button" 
          className="close" 
          aria-hidden="true">
              &times;
      </button>
      {text}
    </div>
  )
}
