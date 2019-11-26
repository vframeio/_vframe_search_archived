 import React, { Component } from 'react'
import { Route, Link } from 'react-router-dom'

import { MenuButton, FileInput } from '../../../common'

export default class TaskMenu extends Component {
  render() {
    return (
      <div className='menuButtons'>
        <Route exact path='/task/' component={TaskIndexMenu} />
        <Route exact path='/task/tests/' component={TaskIndexMenu} />
      </div>
    )
  }
}

const TaskIndexMenu = () => ([
  <MenuButton key='list' name="list" href="/task/" />,
])

  // <MenuButton key='test' name="test" href="/task/tests/" />,
