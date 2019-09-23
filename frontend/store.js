import { applyMiddleware, compose, combineReducers, createStore } from 'redux'
import { connectRouter, routerMiddleware } from 'connected-react-router'
import { createBrowserHistory } from 'history'
import thunk from 'redux-thunk'
import { login } from './util'

import taskReducer from './views/task/task.reducer'
import mediaReducer from './views/media/media.reducer'
import searchReducer from './views/search/search.reducer'
import socketReducer from './socket/socket.reducer'
import uploadReducer from './views/upload/upload.reducer'
import featureReducer from './views/feature/feature.reducer'
import modelzooReducer from './views/modelzoo/modelzoo.reducer'
import dashboardReducer from './views/dashboard/dashboard.reducer'
import collectionReducer from './views/collection/collection.reducer'
import collectionMediaReducer from './views/collectionMedia/collectionMedia.reducer'

const rootReducer = combineReducers({
  auth: (state = {}) => state,
  task: taskReducer,
  media: mediaReducer,
  search: searchReducer,
  socket: socketReducer,
  upload: uploadReducer,
  feature: featureReducer,
  modelzoo: modelzooReducer,
  dashboard: dashboardReducer,
  collection: collectionReducer,
  collectionMedia: collectionMediaReducer,
})

function configureStore(initialState = {}, history) {
  const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose

  const store = createStore(
    connectRouter(history)(rootReducer), // new root reducer with router state
    initialState,
    composeEnhancers(
      applyMiddleware(
        thunk,
        routerMiddleware(history)
      ),
    ),
  )

  return store
}

const history = createBrowserHistory()
const store = configureStore({}, history)

export { store, history }
