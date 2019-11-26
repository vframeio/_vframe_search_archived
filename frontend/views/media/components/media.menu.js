import React, { Component } from 'react'
import { Route, Link } from 'react-router-dom'

import { MenuButton, FileInput } from '../../../common'

export default class MediaMenu extends Component {
  render() {
    return (
      <div className='menuButtons'>
        <Route exact path='/media/id/:id/' component={MediaShowMenu} />
        <Route exact path='/media/sha256/:hash/' component={MediaShowMenu} />
        <Route exact path='/media/' component={MediaIndexMenu} />
      </div>
    )
  }
}

const MediaIndexMenu = () => ([
  <MenuButton key='back' name="back" />,
])

const MediaShowMenu = (props) => ([
  <MenuButton key='back' name="back" />,
  <MenuButton key='search' name="search" href={'/search' + props.location.pathname.replace('id/', '')} />,
])
