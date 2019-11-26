import React, { Component } from 'react'
import { Route, Link } from 'react-router-dom'
import { connect } from 'react-redux'

import { formatDateTime } from '../../../util'
import { SmallMenuButton } from '../../../common'
import CollectionMediaToggle from '../../collectionMedia/collectionMedia.toggle.js'

class MediaList extends Component {
  render() {
    const { searchOptions, els, order, lookup, collectionMedia } = this.props
    return (
      <div className={'results ' + searchOptions.thumbnailSize}>
        {els
          ? els.map(el => <MediaItem key={el.id} data={el} collectionMedia={collectionMedia} />)
          : order.map(id => <MediaItem key={id} data={lookup[id]} collectionMedia={collectionMedia} />)
        }
      </div>
    )
  }
}

const MediaItem = ({ data, collectionMedia }) => {
  return (
    <div className='cell'>
      <div className='img'>
        <Link to={"/media/id/" + data.id + "/"}>
          <img src={data.url} alt={"Media"} />
        </Link>
      </div>
      <div className='meta center'>
        <div className='row'>
          <CollectionMediaToggle collectionMedia={collectionMedia} id={data.id} />
          <SmallMenuButton name="search" href={"/search/media/" + data.id + "/"} />
        </div>
        <div>
          {data.username}
        </div>
        <div>
          {formatDateTime(data.created_at)}
        </div>
      </div>
    </div>
  )
}

const mapStateToProps = state => ({
  searchOptions: state.search.options,
  collectionMedia: state.collectionMedia,
})

const mapDispatchToProps = dispatch => ({
  // searchActions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(MediaList)
