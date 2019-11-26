import { bindActionCreators } from 'redux'
import { actions as crudActions } from './api'

import * as taskActions from './views/task/task.actions'
import * as searchActions from './views/search/search.actions'
import * as socketActions from './socket/socket.actions'
import * as dashboardActions from './views/dashboard/dashboard.actions'
import * as collectionMediaActions from './views/collectionMedia/collectionMedia.actions'

import { store } from './store'

export default
    Object.keys(crudActions)
          .map(a => [a, crudActions[a]])
          .concat([
            ['collectionMedia', collectionMediaActions],
            ['dashboard', dashboardActions],
            ['search', searchActions],
            ['task', taskActions],
          ])
          .map(p => [p[0], bindActionCreators(p[1], store.dispatch)])
          .concat([
            ['socket', socketActions],
          ])
          .reduce((a,b) => (a[b[0]] = b[1])&&a,{})