import React, { Component } from 'react'
import { Route, Link } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import actions from '../../../actions'
import { Loader, TableObject } from '../../../common'
import { TaskInfo } from '../components/task.info'

class TaskTests extends Component {
  state = {
    updating: false,
  }

  startTask() {
    actions.task.long_task()
  }

  ping() {
    actions.task.ping()
  }

  updateIndex() {
    actions.task.update_index()
    this.setState({ updating: true })
  }

  render() {
    const { tasks, pingpong } = this.props
    const taskIds = Object.keys(tasks || {}).sort()
    return (
      <div>
        <h1>Task Manager</h1>
        <div className='buttons'>
          <button onClick={this.startTask.bind(this)}>Run test task</button>
          <button disabled={this.state.updating} onClick={this.updateIndex.bind(this)}>Update index</button>
          <button onClick={this.ping.bind(this)}>Ping</button>
          <PingPong data={pingpong} />
        </div>

        {!!taskIds.length &&
          <div>
            <h2>Active Tasks</h2>
            <div>
              {taskIds.map(id => <TaskInfo key={id} uuid={id} task={tasks[id]} />)}
            </div>
          </div>
        }
      </div>
    )
  }
}

const PingPong = ({ data }) => {
  if (!data) return null
  const { ping, pong } = data
  if (ping && pong) {
    return <small>Roundtrip {pong - ping} ms</small>
  }
  if (ping) {
    return <small>Ping...</small>
  }
  return null
}

const mapStateToProps = state => ({
  tasks: state.task.tasks,
  pingpong: state.task.pingpong,
})

const mapDispatchToProps = dispatch => ({
  // searchActions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(TaskTests)
