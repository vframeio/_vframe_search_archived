import React, { Component } from 'react'
import { Link } from 'react-router-dom'

import { session } from '../../../session'

import { MenuButton, FileInput } from '../../../common'

export default class QueryMenu extends Component {
  render() {
    const currentCollection = session.get('currentCollection')
    return (
      <div className='menuButtons'>
        <MenuButton name="upload">
          <FileInput onChange={this.props.searchActions.upload} />
        </MenuButton>
        <MenuButton name="saved" href={currentCollection ? "/collection/" + currentCollection + "/show/" : "/collection/"} />
        <MenuButton name="recent" href="/upload/" />
        <MenuButton name="random" href={"/search/random/" + parseInt(Math.random() * (2 ** 30)).toString(16) + "/"} />
      </div>
    )
  }
}

/*
  <MenuButton name="new" href="/collections/new" />
*/
