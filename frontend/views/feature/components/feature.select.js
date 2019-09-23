import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import * as searchActions from '../../search/search.actions'
import * as featureActions from '../feature.actions'

import { Select } from '../../../common'

const loadingOptions = [{ name: 'loading', label: 'Loading features...' }]

export class FeatureSelect extends Component {
  state = {
    loading: true,
    options: loadingOptions,
    currentFeature: 'loading',
  }

  componentDidUpdate(prevProps, props) {
    const { info, feature, modelzoo, currentFeature } = this.props
    let diff = (
      (this.props['feature'] !== prevProps['feature']) ||
      (this.props['modelzoo'] !== prevProps['modelzoo']) ||
      (this.props['info'] !== prevProps['info']) ||
      (this.props['currentFeature'] !== prevProps['currentFeature'])
    )
    const loading = !!(
      modelzoo.loading || !modelzoo.order ||
      feature.loading || !feature.order ||
      info.loading || !info.feature || currentFeature.loading
    )
    if (diff && !loading) {
      if (this.state.options === loadingOptions) {
        this.updateFeatureList()
      } else {
        this.setState({ loading })
      }
    }
  }

  updateFeatureList() {
    const { feature, modelzoo, info } = this.props
    const options = feature.order.map(id => ({
      name: feature.lookup[id].id,
      label: modelzoo.lookup[feature.lookup[id].modelzoo_name].name,
    }))
    const currentFeature = info.feature.id
    this.setState({ loading: false, options, currentFeature })
  }

  changeFeature(name, value) {
    this.setState({ currentFeature: parseInt(value), loading: true })
    this.props.featureActions.load(value)
    .then(() => {
      this.props.searchActions.info(value)
      if (this.props.searchOptions.autoprocess) {
        this.props.searchActions.loadCurrentPath()
      }
    })
  }

  render() {
    const { loading, options, currentFeature } = this.state
    return (
      <Select
        name='currentFeature'
        options={options}
        loading={loading}
        selected={currentFeature}
        onChange={this.changeFeature.bind(this)}
      />
    )
  }
}

const mapStateToProps = state => ({
  currentFeature: state.feature.currentFeature,
  feature: state.feature.index,
  modelzoo: state.modelzoo.index,
  searchOptions: state.search.options,
  info: state.search.info.res || {},
})

const mapDispatchToProps = dispatch => ({
  searchActions: bindActionCreators({ ...searchActions }, dispatch),
  featureActions: bindActionCreators({ ...featureActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(FeatureSelect)
