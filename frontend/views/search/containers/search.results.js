import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import * as searchActions from '../search.actions'
import { Loader } from '../../../common'
import SearchResults from '../components/results.searchResults'
import ResultsOptions from '../components/results.options'

export default class Results extends Component {
  render() {
    const { options, results, query } = this.props
    if (!results.results || !results.results.length) {
      return (
        <section>
          <ResultsOptions />
          {query.loading && <Loader />}
        </section>
      )
    }
    return (
      <section>
        <ResultsOptions />
        <SearchResults {...this.props} />
      </section>
    )
  }
}
