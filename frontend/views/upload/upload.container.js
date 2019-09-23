import React, { Component } from 'react'
import { Route, Link } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import actions from '../../actions'
import * as uploadActions from './upload.actions'

import Sidebar from '../dashboard/components/dashboard.sidebar'
import UploadMenu from './components/upload.menu'
import UploadIndex from './components/upload.index'
import UploadShow from './components/upload.show'

class Container extends Component {
  componentDidMount() {
    actions.upload.index()
  }

  render() {
    return (
      <div className='row upload'>
        <Sidebar />
        <div>
          <Route exact path='/upload/:id/show/' component={UploadShow} />
          <UploadIndex {...this.props} />
        </div>
      </div>
    )
  }
}

/*
        <Route exact path='/collection/:id/show/' component={CollectionShow} />
        <Route exact path='/collection/' component={CollectionIndex} />
*/

const mapStateToProps = state => ({
  upload: state.upload,
  searchOptions: state.search.options,
})

const mapDispatchToProps = dispatch => ({
  uploadActions: bindActionCreators({ ...uploadActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(Container)
