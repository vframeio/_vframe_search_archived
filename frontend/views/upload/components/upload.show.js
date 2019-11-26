import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'

import actions from '../../../actions'
import { formatDate, formatTime, formatAge, uploadUri } from '../../../util'
import { history } from '../../../store'
import { Loader, MenuButton } from '../../../common'

class UploadShow extends Component {
  componentDidMount() {
    actions.upload.show(this.props.match.params.id)
  }

  componentDidUpdate(prevProps) {
    if (prevProps.match.params.id !== this.props.match.params.id) {
      actions.upload.show(this.props.match.params.id)
    }
  }

  handleDestroy() {
    const { res: data } = this.props.upload.show
    if (confirm("Really delete this upload?")) {
      actions.upload.destroy(data).then(() => {
        history.push('/upload/')
      })
    }
  }

  render() {
    const { show, destroy } = this.props.upload
    if (show.loading || destroy.loading) {
      return <Loader />
    }
    if (!show.loading && !show.res || show.not_found) {
      return <div className='gray'>Upload {this.props.match.params.id} not found</div>
    }
    const { res: data } = show
    return (
      <section className="row uploadShow">
        <div className="menuButtons">
          <MenuButton name="delete" onClick={this.handleDestroy.bind(this)} />
          <MenuButton name="search" href={'/search/upload/' + data.id + '/'} />
        </div>
        <div>
          <img src={uploadUri(data)} />
          <div className='byline'>
            {'Uploaded by '}
            {data.username}
            {' on '}
            {formatDate(data.created_at)}
            {' at '}
            {formatTime(data.created_at)}
            {'. '}
          </div>
        </div>
      </section>
    )
  }
}

const mapStateToProps = state => ({
  upload: state.upload,
})

const mapDispatchToProps = dispatch => ({
  // searchActions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(UploadShow)
