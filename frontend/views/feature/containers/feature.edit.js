import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'

import { history } from '../../../store'
import actions from '../../../actions'

import { Loader } from '../../../common'

import FeatureForm from '../components/feature.form'

class FeatureNew extends Component {
  componentDidMount() {
    actions.feature.show(this.props.match.params.id)
  }

  handleSubmit(data) {
    actions.feature.update(data)
      .then(response => {
        // response
        console.log(response)
        history.push('/feature/' + data.id + '/show/')
      })
  }

  render() {
    const { show } = this.props.feature
    if (show.loading || !show.res) {
      return (
        <div className='form'>
          <h1>Loading...</h1>
          <Loader />
        </div>
      )
    }
    return (
      <FeatureForm
        data={show.res}
        onSubmit={this.handleSubmit.bind(this)}
        {...this.props}
      />
    )
  }
}

const mapStateToProps = state => ({
  feature: state.feature,
  modelzoo: state.modelzoo,
})

const mapDispatchToProps = dispatch => ({
  // searchActions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(FeatureNew)
