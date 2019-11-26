import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'

import actions from '../../../actions'
import { formatDate, formatTime, formatAge } from '../../../util'
import { history } from '../../../store'
import { Loader } from '../../../common'
import MediaList from '../../media/components/media.list.js'
import ReactMarkdown from 'react-markdown'

class CollectionShow extends Component {
  componentDidMount() {
    actions.collection.show(this.props.match.params.id)
  }

  render() {
    const { show, destroy } = this.props.collection
    if (show.loading || destroy.loading) {
      return <Loader />
    }
    if (!show.loading && !show.res || show.not_found) {
      return <div className='gray'>Collection {this.props.match.params.id} not found</div>
    }
    const { res: data } = show
    const { collectionMedia } = this.props
    return (
      <div>
        <h1>{data.title}</h1>
        <div className='byline'>
          {'Created by '}
          {data.username}
          {' on '}
          {formatDate(data.created_at)}
          {' at '}
          {formatTime(data.created_at)}
          {'. '}
          {!!data.updated_at && "Last updated " + formatAge(data.updated_at)}
        </div>
        {!!(data.notes || "").length && (
          <ReactMarkdown source={data.notes} />
        )}
        <MediaList els={data.media} collectionMedia={collectionMedia === data.id ? collectionMedia : {}}/>
      </div>
    )
  }
}

const mapStateToProps = state => ({
  collection: state.collection,
  collectionMedia: state.collectionMedia,
})

const mapDispatchToProps = dispatch => ({
  // searchActions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(CollectionShow)
