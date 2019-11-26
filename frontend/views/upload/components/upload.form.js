import React, { Component } from 'react'
import { Link } from 'react-router-dom'

import { MenuButton, FileInput } from '../../../common'

export default class UploadForm extends Component {
  render() {
    return (
      <div className='uploadForm'>
        <MenuButton name="upload" label={false}>
          <FileInput onChange={this.props.uploadActions.upload} />
        </MenuButton>
      </div>
    )
  }
}
