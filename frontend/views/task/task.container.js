import React, { Component } from 'react'
import { Route, Link } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import actions from '../../actions'

import Sidebar from '../dashboard/components/dashboard.sidebar'

import TaskIndex from './containers/task.index'
import TaskTests from './containers/task.tests'
import TaskMenu from './components/task.menu'

class Container extends Component {
  render() {
    return (
      <div className="taskContainer row">
        <Sidebar />
        <div className='row'>
          <Route exact path='/task/' component={TaskTests} />
        </div>
      </div>
    )
  }
}
          // <TaskMenu />
          // <Route exact path='/task/tests/' component={TaskTests} />

const mapStateToProps = state => ({
  task: state.task,
})

const mapDispatchToProps = dispatch => ({
  // searchActions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(Container)
