import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'

import { MenuButton, Loader } from '../../../common'

import MediaIndexOptions from '../components/media.indexOptions'
import MediaMenu from '../components/media.menu'
import MediaList from '../components/media.list'
import CollectionMediaToggle from '../../collectionMedia/collectionMedia.toggle.js'

class MediaIndex extends Component {
  render() {
    const { searchOptions } = this.props
    const { options } = this.props.media
    const { loading, lookup, order } = this.props.media.index
    if (loading) {
      return (
        <section>
          <MediaIndexOptions />
          <div className="row">
            <Loader />
          </div>
        </section>
      )
    }
    if (!lookup || !order.length) {
      return (
        <section>
          <MediaIndexOptions />
          <div className="row">
            <MediaMenu />
            <p className='gray'>
              {"No media"}
            </p>
          </div>
        </section>
      )
    }
    return (
      <section>
        <MediaIndexOptions />
        <div className="row">
          <MediaMenu />
          <MediaList order={order} lookup={lookup} />
        </div>
      </section>
    )
  }
}

const mapStateToProps = state => ({
  media: state.media,
})

const mapDispatchToProps = dispatch => ({
  // searchActions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(MediaIndex)
