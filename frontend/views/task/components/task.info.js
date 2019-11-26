import React, { Component } from 'react'
import { TaskProgress } from '../components/task.progress'

export const TaskInfo = ({ uuid, task }) => {
  const { debug, error, progress } = task
  return (
    <div className='row taskInfo'>
      {progress && <TaskProgress progress={progress} />}
      {debug && <div className='debug'>{debug}</div>}
      {error && <div className='error'>{error}</div>}
    </div>
  )
}
