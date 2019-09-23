import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'

import actions from '../../../actions'

import { formatDateTime } from '../../../util'
import { Loader, TableIndex } from '../../../common'

const collectionFields = [
  { name: 'title', type: 'title', link: row => '/collection/' + row.id + '/show/' },
  { name: 'username', type: 'string' },
  { name: 'date', type: 'date', valueFn: row => formatDateTime(row.updated_at || row.created_at) },
  { name: 'notes', type: 'text', valueFn: row => (row.notes || "").trim().split('\n')[0].replace(/^#+/, '').substr(0, 100) },
]

class CollectionIndex extends Component {
  render() {
    return (
      <TableIndex
        title="Collections"
        actions={actions.collection}
        data={this.props.collection.index}
        fields={collectionFields}
      />
    )
  }
}

const mapStateToProps = state => ({
  collection: state.collection,
})

const mapDispatchToProps = dispatch => ({
  // searchActions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(CollectionIndex)
