import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'

import { history } from '../../../store'
import actions from '../../../actions'

import { Loader } from '../../../common'

import CollectionForm from '../components/collection.form'

class CollectionNew extends Component {
  componentDidMount() {
    actions.collection.show(this.props.match.params.id)
  }

  handleSubmit(data) {
    actions.collection.update(data)
      .then(response => {
        // response
        console.log(response)
        history.push('/collection/' + data.id + '/show/')
      })
  }

  render() {
    const { show } = this.props.collection
    if (show.loading || !show.res) {
      return (
        <div className='form'>
          <h1>Loading...</h1>
          <Loader />
        </div>
      )
    }
    return (
      <CollectionForm
        data={show.res}
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
