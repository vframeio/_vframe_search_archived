import React, { Component } from 'react'
import { Link } from 'react-router-dom'

import { uploadUri, formatDateTime } from '../../../util'
import { MenuButton, SmallMenuButton, Loader } from '../../../common'

import UploadIndexOptions from './upload.indexOptions'
import UploadMenu from './upload.menu'

import CollectionMediaToggle from '../../collectionMedia/collectionMedia.toggle.js'

// const { result, collectionLookup } = this.props

export default class UploadIndex extends Component {
  render() {
    const { searchOptions, uploadActions } = this.props
    const { options } = this.props.upload
    const { loading, lookup, order } = this.props.upload.index
    if (loading) {
      return (
        <section>
          <UploadIndexOptions />
          <div className="row">
            <Loader />
          </div>
        </section>
      )
    }
    if (!lookup || !order.length) {
      return (
        <section>
          <UploadIndexOptions />
          <div className="row">
            <UploadMenu uploadActions={uploadActions} />
            <p className='gray'>
              {"No uploads"}
            </p>
          </div>
        </section>
      )
    }
    return (
      <section>
        <UploadIndexOptions />
        <div className="row">
          <UploadMenu uploadActions={uploadActions} />
          <div className={'results ' + searchOptions.thumbnailSize}>
            {order.map(id => <UploadItem key={id} data={lookup[id]} />)}
          </div>
        </div>
      </section>
    )
  }
}

const UploadItem = ({ data }) => {
  // console.log(data)
  const imageUri = uploadUri(data)
  return (
    <div className='cell'>
      <div className='img'>
        <Link to={"/upload/" + data.id + "/show/"}>
          <img src={imageUri} alt={"Uploaded image"} />
        </Link>
      </div>
      <div className='meta center'>
        <div className='row'>
          <SmallMenuButton name="search" href={"/search/upload/" + data.id + "/"} />
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

          // <CollectionMediaToggle collectionLookup={collectionLookup} id={result.media.id} />
