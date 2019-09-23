import React, { Component } from 'react'
import { Route } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import Sidebar from './components/dashboard.sidebar'
import DashboardIndex from './containers/dashboard.index'

export default class Container extends Component {
  render() {
    return (
      <div className='dashboard'>
        <Sidebar />
        <Route exact path='/dashboard/' component={DashboardIndex} />
      </div>
    )
  }
}
