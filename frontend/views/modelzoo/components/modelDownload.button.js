import React, { Component } from 'react'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import actions from '../../../actions'

import { TaskProgress } from '../../task/components/task.progress'

class ModelDownloadButton extends Component {
  state = {
    uuid: null
  }
  
  handleClick() {
    const { id } = this.props
    console.log(id)
    actions.task.download_model(id)
    .then(data => {
      console.log(data)
      this.setState({ uuid: data.uuid })
    })
  }

  render() {
    const { uuid } = this.state
    if (uuid && uuid in this.props.tasks) {
      return (
        <div>
          <TaskProgress progress={this.props.tasks[uuid].progress} />
        </div>
      )
    } else {
      return (
        <div>
          <button onClick={() => this.handleClick()}>Download model</button>
        </div>
      )
    }
  }
}


const mapStateToProps = state => ({
  tasks: state.task.tasks
})

const mapDispatchToProps = dispatch => ({
})

export default connect(mapStateToProps, mapDispatchToProps)(ModelDownloadButton)
