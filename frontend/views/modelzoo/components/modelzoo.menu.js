 import React, { Component } from 'react'
import { Route, Link } from 'react-router-dom'

import { MenuButton, FileInput } from '../../../common'

export default class ModelZooMenu extends Component {
  render() {
    return (
      <div className='menuButtons'>
        <Route exact path='/modelzoo/:id/show/' component={ModelZooShowMenu} />
        <Route exact path='/modelzoo/' component={ModelZooIndexMenu} />
      </div>
    )
  }
}

const ModelZooIndexMenu = () => ([
  <MenuButton key='index' name="list" href="/modelzoo/" />
])

const ModelZooShowMenu = () => ([
  <MenuButton key='back' name="back" href="/modelzoo/" />
])
