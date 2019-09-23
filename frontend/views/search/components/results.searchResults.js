import React, { Component } from 'react'
import { Link } from 'react-router-dom'

import SearchResult from '../components/results.searchResult'

export default class SearchResults extends Component {
  render(){
    const { options, results, collectionMedia } = this.props
    return (
      <div className={'results ' + options.thumbnailSize}>
        {results.results.map(result => <SearchResult key={result.media.id} result={result} collectionMedia={collectionMedia} />)}
      </div>
    )
  }
}
