 import React, { Component } from 'react'
import { Route, Link } from 'react-router-dom'

import { MenuButton, FileInput } from '../../../common'

export default class FeatureMenu extends Component {
  render() {
    return (
      <div className='menuButtons'>
        <Route exact path='/feature/:id/show/' component={FeatureShowMenu} />
        <Route exact path='/feature/:id/edit/' component={FeatureEditMenu} />
        <Route exact path='/feature/new/' component={FeatureNewMenu} />
        <Route exact path='/feature/' component={FeatureIndexMenu} />
      </div>
    )
  }
}

const FeatureIndexMenu = () => ([
  <MenuButton key='new' name="new" href="/feature/new/" />,
])

const FeatureShowMenu = (props) => ([
  <MenuButton key='back' name="back" />,
  <MenuButton key='edit' name="edit" href={"/feature/" + props.match.params.id + "/edit/"} />,
])

const FeatureNewMenu = (props) => ([
  <MenuButton key='back' name="back" />,
])

const FeatureEditMenu = (props) => ([
  <MenuButton key='back' name="back" />,
])
