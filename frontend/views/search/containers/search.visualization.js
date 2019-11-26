import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import * as searchActions from '../search.actions'

class Visualization extends Component {
  render() {
    return (
      <div>
      </div>
    )
  }
}

const mapStateToProps = state => ({
  query: state.search.query.query,
  results: state.search.query.results,
  options: state.search.options,
})

const mapDispatchToProps = dispatch => ({
  searchActions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(Visualization)
