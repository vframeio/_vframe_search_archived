import React, { Component } from 'react'
import { Link, withRouter } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import QueryMenu from '../components/query.menu'
import QueryImage from '../components/query.image'
import QueryOptions from '../components/query.options'

export default class Query extends Component {
  render() {
    return (
      <div className='query'>
        <div className='row'>
          <QueryMenu {...this.props} />
          <QueryImage {...this.props} />
          <QueryOptions {...this.props} />
        </div>
      </div>
    )
  }
}
