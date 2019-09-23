import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'

import { history } from '../../../store'
import actions from '../../../actions'

import CollectionForm from '../components/collection.form'

class CollectionNew extends Component {
  handleSubmit(data) {
    console.log(data)
    actions.collection.create(data)
      .then(res => {
        console.log(res)
        if (res.res && res.res.id) {
          history.push('/collection/' + res.res.id + '/show/')
        }
      })
      .catch(err => {
        console.error('error')
      })
  }

  render() {
    return (
      <CollectionForm
        isNew
        data={{}}
        onSubmit={this.handleSubmit.bind(this)}
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

export default connect(mapStateToProps, mapDispatchToProps)(CollectionNew)
