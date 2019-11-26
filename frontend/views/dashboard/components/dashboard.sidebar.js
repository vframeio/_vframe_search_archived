import React, { Component } from 'react'
import { NavLink } from 'react-router-dom'

export default function Sidebar(props) {
  return (
    <div className='sidebarContainer'>
      <ul className='sidebar'>
        <NavLink to="/dashboard/"><li>Dashboard</li></NavLink>
        <NavLink to="/task/"><li>Task Manager</li></NavLink>
        <NavLink to="/modelzoo/"><li>Model Zoo</li></NavLink>
        <NavLink to="/feature/"><li>Feature Indexes</li></NavLink>
        <NavLink to="/upload/"><li>Upload Manager</li></NavLink>
      </ul>
    </div>
  )
}
