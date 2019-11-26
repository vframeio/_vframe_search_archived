import React, { Component } from 'react'
import { Route, Link } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import actions from '../../actions'

import Sidebar from '../dashboard/components/dashboard.sidebar'

import FeatureNew from './containers/feature.new'
import FeatureShow from './containers/feature.show'
import FeatureIndex from './containers/feature.index'
import FeatureEdit from './containers/feature.edit'

import FeatureMenu from './components/feature.menu'

class Container extends Component {
  componentDidMount() {
    if (!this.props.feature.index.lookup) {
      actions.feature.index()
    }
    if (!this.props.modelzoo.index.lookup) {
      actions.modelzoo.index()
    }
  }

  render() {
    return (
      <div className="feature row">
        <Sidebar />
        <div className='row'>
          <FeatureMenu />
          <Route exact path='/feature/new/' component={FeatureNew} />
          <Route exact path='/feature/:id/edit/' component={FeatureEdit} />
          <Route exact path='/feature/:id/show/' component={FeatureShow} />
          <Route exact path='/feature/' component={FeatureIndex} />
        </div>
      </div>
    )
  }
}

const mapStateToProps = state => ({
  feature: state.feature,
  modelzoo: state.modelzoo,
})

const mapDispatchToProps = dispatch => ({
  // searchActions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(Container)
