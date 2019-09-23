import React, { Component } from 'react'
import { Route, Link } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import actions from '../../actions'
import * as mediaActions from './media.actions'

import MediaMenu from './components/media.menu'
import MediaIndex from './containers/media.index'
import MediaShow from './containers/media.show'

class Container extends Component {
  componentDidMount() {
  }

  render() {
    return (
      <div>
        <section className="media row">
        <MediaMenu />
        <Route exact path='/media/id/:id/' component={MediaShow} />
        <Route exact path='/media/hash/:hash/' component={MediaShow} />
        <Route exact path='/media/' component={MediaIndex} />
        </section>
      </div>
    )
  }
}

/*
        <Route exact path='/collection/:id/show/' component={CollectionShow} />
        <Route exact path='/collection/' component={CollectionIndex} />
*/

const mapStateToProps = state => ({
  media: state.media,
})

const mapDispatchToProps = dispatch => ({
  mediaActions: bindActionCreators({ ...mediaActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(Container)
