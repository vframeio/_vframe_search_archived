import React, { Component } from 'react'

export const TaskProgress = ({ data, progress }) => {
  const { current, total, message } = progress || data.progress || {}
  return (
    <div className='progress'>
      <div>
        {current}{' / '}{total} - {message}
      </div>
      <div className='bar'>
        <div className='percentage' style={{ width: Math.round(100 * current / total) + '%' }} />
      </div>
    </div>
  )
}
