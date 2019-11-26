import React, { Component } from 'react'
import { Route, Link } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import actions from '../../actions'

import Sidebar from '../dashboard/components/dashboard.sidebar'

import ModelZooShow from './containers/modelzoo.show'
import ModelZooIndex from './containers/modelzoo.index'
import ModelZooMenu from './components/modelzoo.menu'

class Container extends Component {
  componentDidMount() {
    if (!this.props.modelzoo.index.lookup) {
      actions.modelzoo.index()
    }
  }

  render() {
    return (
      <div className="modelzoo row">
        <Sidebar />
        <div className='row'>
          <ModelZooMenu />
          <Route exact path='/modelzoo/:id/show/' component={ModelZooShow} />
          <Route exact path='/modelzoo/' component={ModelZooIndex} />
        </div>
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

export default connect(mapStateToProps, mapDispatchToProps)(Container)
