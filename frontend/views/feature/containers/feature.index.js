import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'

import actions from '../../../actions'

import { formatDateTime } from '../../../util'
import { Loader, TableIndex } from '../../../common'

class FeatureIndex extends Component {
  state = {
    hasLookups: false,
  }
  
  componentDidUpdate(prevProps) {
    if (this.props.modelzoo.index.order && this.props.feature.index.order && !this.state.hasLookups) {
      const { order: featureOrder, lookup: featureLookup } = this.props.feature.index
      const { lookup: modelzooLookup } = this.props.modelzoo.index
      featureOrder.forEach(id => {
        const item = featureLookup[id]
        item['modelzoo'] = item.modelzoo_name in modelzooLookup ? modelzooLookup[item.modelzoo_name] : {}
      })
      this.setState({ hasLookups: true })
    }
  }

  render() {
    const { lookup: modelzooLookup } = this.props.modelzoo.index
    return (
      <TableIndex
        title="Feature Indexes"
        actions={actions.feature}
        data={this.props.feature.index}
        fields={[
          { name: 'model', type: 'title', title: 'Model', width: '20rem',
            link: row => '/feature/' + row.id + '/show/',
            valueFn: row => row.modelzoo && row.modelzoo.name,
          },
          { name: 'index_type', type: 'str', width: '8rem', },
          { name: 'last indexed', type: 'date', valueFn: row => row.indexed_at ? formatDateTime(row.indexed_at) : 'never' },
          { name: 'task_type', type: 'str', width: '8rem',
            valueFn: row => row.modelzoo && row.modelzoo.task_type,
          },
          { name: 'framework', type: 'str', width: '6rem',
            valueFn: row => row.modelzoo && row.modelzoo.framework,
          },
          { name: 'downloaded', 'title': 'Dl\'ed?', type: 'bool',
            valueFn: row => row.modelzoo && row.modelzoo.downloaded,
          },
          { name: 'active', type: 'bool' },
        ]}
      />
    )
  }
}

const getModelZooName = (lookup, name) => name in lookup ? lookup[name].name : ' '

const mapStateToProps = state => ({
  feature: state.feature,
  modelzoo: state.modelzoo,
})

const mapDispatchToProps = dispatch => ({
  // searchActions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(FeatureIndex)
