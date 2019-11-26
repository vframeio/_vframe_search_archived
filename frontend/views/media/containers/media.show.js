import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'

import actions from '../../../actions'
import { formatDate, formatTime, formatAge } from '../../../util'
import { history } from '../../../store'
import { Loader, MenuButton } from '../../../common'
import MediaList from '../components/media.list'

class MediaShow extends Component {
  componentDidMount() {
    this.loadPath()
  }

  componentDidUpdate(prevProps) {
    if (prevProps.match.url !== this.props.match.url) {
      this.loadPath()
    }
  }

  loadPath(){
    const { params, url } = this.props.match
    const [ slash, media, tag, id, ...rest ] = url.split('/')
    switch (tag) {
      case 'sha256':
      case 'id':
      default:
        actions.media.show(tag + '/' + id)
    }
  }

  handleDestroy() {
    const { res: data } = this.props.media.show
    if (confirm("Really delete this media?")) {
      actions.media.destroy(data).then(() => {
        history.push('/media/')
      })
    }
  }

  goSearch() {
    const { res: data } = this.props.media.show
    history.push('/search/media/' + data.id + '/')
  }

  render() {
    const { show, destroy } = this.props.media
    if (show.loading || destroy.loading) {
      return <Loader />
    }
    if (!show.loading && !show.res || show.not_found) {
      return <div className='gray'>Media {this.props.match.params.id} not found</div>
    }
    const { el: data, siblings } = show.res
    return (
      <div>
        <div>
          <img className='mediaShow' src={data.url} />
          <div className='byline'>
            {'Imported '}
            {formatDate(data.created_at)}
            {' at '}
            {formatTime(data.created_at)}
            {'. '}
          </div>
        </div>
        <MediaList els={siblings} />
      </div>
    )
  }
}

const mapStateToProps = state => ({
  media: state.media,
})

const mapDispatchToProps = dispatch => ({
  // searchActions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(MediaShow)
