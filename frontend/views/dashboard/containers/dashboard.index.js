import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'

import actions from '../../../actions'

import { formatDateTime } from '../../../util'
import { Loader, TableIndex } from '../../../common'
import { TaskInfo } from '../../task/components/task.info'

class DashboardIndex extends Component {
  componentDidMount() {
    // if (!this.props.dashboard.mediaInfo && !this.props.dashboard.mediaInfo.loading) {
    actions.dashboard.mediaInfo()
    actions.collection.index()
    actions.search.info()
    // }
  }
  render() {
    const { collection, modelzoo, feature, dashboard, socket, tasks } = this.props
    const collectionCount = collection.order ? collection.order.length : ''
    const modelzooCount = modelzoo.order ? modelzoo.order.length : ''
    const featureCount = feature.order ? feature.order.length : ''
    const mediaCount = (dashboard.mediaInfo && dashboard.mediaInfo.res) ? dashboard.mediaInfo.res.mediaCount : ''
    const uploadCount = (dashboard.mediaInfo && dashboard.mediaInfo.res) ? dashboard.mediaInfo.res.uploadCount : ''
    const freeSpace = (dashboard.mediaInfo && dashboard.mediaInfo.res) ? (dashboard.mediaInfo.res.freeSpace.toFixed(1) + ' GB') : ''
    const taskIds = Object.keys(tasks || {}).sort()
    return (
      <div>
        <h1>Dashboard</h1>
        <h2>Statistics</h2>
        <div className='rows'>
          <Statistic name='Media' value={mediaCount} />
          <Statistic name='Uploads' value={uploadCount} />
          <Statistic name='Collections' value={collectionCount} />
          <Statistic name='Models in Zoo' value={modelzooCount} />
          <Statistic name='Feature Indexes' value={featureCount} />
          <Statistic name='Disk free space' value={freeSpace} />
        </div>

        <h2>Socket</h2>
        <div className='rows'>
          <Statistic name='Status' value={socket.status} />
        </div>

        {taskIds.length ?
          <div>
            <h2>Tasks</h2>
            <div>
              {taskIds.map(id => <TaskInfo key={id} uuid={id} task={tasks[id]} />)}
            </div>
          </div>
          :
          <div>
            <h2>Background workers</h2>
            <span className='gray'>No active jobs</span>
          </div>
        }
      </div>
    )
  }
}

const Statistic = ({ name, value }) => (
  <div className='row'>
    <div className='title'>{name}</div>
    <div className='int'>{value}</div>
  </div>
)

const mapStateToProps = state => ({
  collection: state.collection.index,
  feature: state.feature.index,
  modelzoo: state.modelzoo.index,
  dashboard: state.dashboard,
  tasks: state.task.tasks,
  search: state.search,
  socket: state.socket,
})

const mapDispatchToProps = dispatch => ({
})

export default connect(mapStateToProps, mapDispatchToProps)(DashboardIndex)
