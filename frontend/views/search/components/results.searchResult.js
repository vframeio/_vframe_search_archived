import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { SmallMenuButton } from '../../../common'

import CollectionMediaToggle from '../../collectionMedia/collectionMedia.toggle.js'

export default class SearchResult extends Component {
  render() {
    const { result, collectionMedia } = this.props
    return (
      <div>
        <img src={result.media.url} />
        <div className='meta center'>
          <div className='row'>
            <CollectionMediaToggle collectionMedia={collectionMedia} id={result.media.id} />
            <SmallMenuButton name="open_in_new" href={"/media/id/" + result.media.id + "/"} />
            <SmallMenuButton name="search" href={"/search/media/" + result.media.id + "/"} />
          </div>
          <span>{result.score.toFixed(2)}</span>
        </div>
      </div>
    )
  }
}
