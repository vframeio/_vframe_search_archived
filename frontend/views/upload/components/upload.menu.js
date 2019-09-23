import React, { Component } from 'react'
import { Link } from 'react-router-dom'

import { MenuButton, FileInput } from '../../../common'

import actions from '../../../actions'

export default class UploadMenu extends Component {
  render() {
    return (
      <div className='menuButtons'>
        <MenuButton name="upload">
          <FileInput onChange={this.props.uploadActions.upload} />
        </MenuButton>
      </div>
    )
  }
}
