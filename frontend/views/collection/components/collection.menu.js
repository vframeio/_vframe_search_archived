import React, { Component } from 'react'
import { Route, Link } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import { saveAs } from 'file-saver'

import { MenuButton, MenuRoute, FileInput } from '../../../common'
import actions from '../../../actions'

class CollectionMenu extends Component {
  render() {
    return (
      <div className='menuButtons'>
        <MenuRoute exact path='/collection/:id/show/' component={CollectionShowMenu} props={this.props} />
        <Route exact path='/collection/:id/edit/' component={CollectionEditMenu} />
        <Route exact path='/collection/new/' component={CollectionNewMenu} />
        <Route exact path='/collection/' component={CollectionIndexMenu} />
      </div>
    )
  }
}

const CollectionIndexMenu = () => ([
  <MenuButton key='back' name="back" />,
  <MenuButton key='new' name="new" href="/collection/new/" />,
])

const CollectionShowMenu = (props) => ([
  <MenuButton key='back' name="back" />,
  <MenuButton key='list' name="list" href="/collection/" />,
  <MenuButton key='edit' name="edit" href={"/collection/" + props.match.params.id + "/edit/"} />,
  <MenuButton key='save' name="save" onClick={() => {
    // const { res: collection } = props.collection.show
    // const fn = collection.title + '.json'
    // const blob = new Blob([
    //   JSON.stringify(props.collection.show.res, null, 2)
    // ], { type: "text/json;charset=utf-8" })
    // saveAs(blob, fn)
    window.open('/api/v1/collection/' + props.match.params.id + '/export/?redirect=1')
      // .then(req => req.json())
      // .then(data => {
      //   console.log(data.url)
      //   window.open(data.url)
      // })
      // .catch(e => console.error(e))
  }} />,
  <MenuButton key='delete' name="delete" onClick={() => {
    const { res: collection } = props.collection.show
    if (confirm("Really delete this collection?")) {
      actions.collection.destroy(collection).then(() => {
        history.push('/collection/')
      })
    }
  }} />
])

const CollectionNewMenu = (props) => ([
  <MenuButton key='back' name="back" href={"/collection/"} />,
])

const CollectionEditMenu = (props) => ([
  <MenuButton key='back' name="back" href={"/collection/" + props.match.params.id + "/show/"} />,
])

const mapStateToProps = state => ({
  collection: state.collection,
})

const mapDispatchToProps = dispatch => ({
  // searchActions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(CollectionMenu)
