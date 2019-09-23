import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import actions from '../../actions'

import * as searchActions from './search.actions'
import { Query, Visualization, Results, Router } from './containers'

class SearchContainer extends Component {
  componentDidMount() {
    actions.search.info()
    if (this.props.options.autoprocess) {
      this.props.searchActions.loadCurrentPath()
    }
  }
  componentDidUpdate(prevProps) {
    if (this.props.location.pathname !== prevProps.location.pathname && this.props.options.autoprocess) {
      this.props.searchActions.loadCurrentPath()
    }
  }
  render() {
    return (
      <div>
        <Query {...this.props} />
        <Visualization {...this.props} />
        <Results {...this.props} />
      </div>
    )
  }
}

const mapStateToProps = state => ({
  info: state.search.info,
  query: state.search.query,
  results: state.search.results,
  infer: state.search.infer,
  options: state.search.options,
  feature: state.feature.index,
  modelzoo: state.modelzoo.index,
  collectionMedia: state.collectionMedia,
})

const mapDispatchToProps = dispatch => ({
  searchActions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(SearchContainer)
