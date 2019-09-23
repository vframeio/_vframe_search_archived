import React, { Component } from 'react'
import { ConnectedRouter } from 'connected-react-router'
import { Route, Switch } from 'react-router'

import { Header } from './common'

import actions from './actions'

import * as views from './views'

const viewList = Object.keys(views).map(name => {
  const view = views[name]
  return (
    <Route key={name} path={'/' + name} component={view} />
  )
})

export default class App extends Component {
  componentDidMount() {
    actions.modelzoo.index()
    actions.feature.index()
    actions.collectionMedia.loadLastCollection()
  }
  render() {
    return (
      <ConnectedRouter history={this.props.history}>
        <div>
          <Header />
          <div className='app'>
            <div className='body'>
              {viewList}
              <Route exact key='root' path='/' render={() => {
                // redirect to search!!
                setTimeout(() => this.props.history.push('/search/'), 10)
                return null
              }} />
            </div>
          </div>
        </div>
      </ConnectedRouter>
    )
  }
}
