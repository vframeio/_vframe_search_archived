import React, { Component } from 'react'
import { Route, Link } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import actions from '../../../actions'
import { Loader, TableObject } from '../../../common'

class TaskIndex extends Component {
  componentDidMount() {
    actions.task.info()
  }

  render() {
    console.log(this.props.info)
    if (!this.props.info.active) {
      return <div><Loader /></div>
    }
    return (
      <div>
        <h1>Tasks</h1>
        <TableObject object={this.props.info.active} tag="Active Tasks" />
        <TableObject object={this.props.info.queued} tag="Queued Tasks" />
        <TableObject object={this.props.info.scheduled} tag="Scheduled Tasks" />
      </div>
    )
  }
}

const mapStateToProps = state => ({
  info: state.task.info,
})

const mapDispatchToProps = dispatch => ({
  // searchActions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(TaskIndex)
