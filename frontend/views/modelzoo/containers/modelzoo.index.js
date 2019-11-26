import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'

import actions from '../../../actions'

import { formatDateTime } from '../../../util'
import { Loader, TableIndex } from '../../../common'

const modelzooFields = [
  { name: 'name', type: 'text', width: '25rem', link: row => '/modelzoo/' + row.key + '/show/' },
  // { name: 'date', type: 'date', valueFn: row => formatDateTime(row.updated_at || row.created_at) },
  // { name: 'task_type', type: 'str', width: '8rem', },
  { name: 'framework', type: 'str', width: '6rem', },
  // { name: 'last_built', type: 'date' },
  { name: 'features', title: "Layer", type: 'text', width: '6rem' },
  { name: 'dims', type: 'str', valueFn: row => (row.dimensions || "") },
  { name: 'downloaded', 'title': 'Dl\'ed?', type: 'bool' },
  { name: 'active', type: 'bool' },
  { name: 'tested', type: 'bool' },
  { name: 'image size', type: 'str', valueFn: row => row.width + 'x' + row.height },
  { name: 'mean', type: 'color' },
]

class ModelZooIndex extends Component {
  state = {
    groups: {},
  }
  componentDidUpdate(prevProps) {
    if (this.props.modelzoo.index !== prevProps.modelzoo.index && this.props.modelzoo.index.order) {
      const { lookup, order } = this.props.modelzoo.index
      const groups = order.reduce((a, id) => {
        const el = lookup[id]
        a[el.task_type] = a[el.task_type] || []
        a[el.task_type].push(el)
        return a
      }, {})
      this.setState({ groups })
    }
  }
  render() {
    const { groups } = this.state
    return (
      <div>
        <TableIndex
          title="Classification"
          actions={actions.modelzoo}
          data={this.props.modelzoo.index}
          els={groups.classification || []}
          fields={modelzooFields}
        />
        <TableIndex
          title="Object Detection"
          actions={actions.modelzoo}
          data={this.props.modelzoo.index}
          els={groups.object_detection || []}
          fields={modelzooFields}
        />
      </div>
    )
  }
}

const mapStateToProps = state => ({
  modelzoo: state.modelzoo,
})

const mapDispatchToProps = dispatch => ({
  // searchActions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(ModelZooIndex)
