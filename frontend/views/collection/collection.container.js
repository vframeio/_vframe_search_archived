import React, { Component } from 'react'
import { Route, Link } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import actions from '../../actions'

import CollectionNew from './containers/collection.new'
import CollectionShow from './containers/collection.show'
import CollectionIndex from './containers/collection.index'
import CollectionEdit from './containers/collection.edit'

import CollectionMenu from './components/collection.menu'

class Container extends Component {
  componentDidMount() {
  }

  render() {
    return (
      <section className="collection row">
        <CollectionMenu />
        <Route exact path='/collection/new/' component={CollectionNew} />
        <Route exact path='/collection/:id/show/' component={CollectionShow} />
        <Route exact path='/collection/:id/edit/' component={CollectionEdit} />
        <Route exact path='/collection/' component={CollectionIndex} />
      </section>
    )
  }
}

const mapStateToProps = state => ({
})

const mapDispatchToProps = dispatch => ({
  // searchActions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(Container)
