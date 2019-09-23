import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'

import { history } from '../../../store'
import actions from '../../../actions'

import FeatureForm from '../components/feature.form'

class FeatureNew extends Component {
  handleSubmit(data) {
    console.log(data)
    actions.feature.create(data)
      .then(res => {
        console.log(res)
        if (res.res && res.res.id) {
          history.push('/feature/' + res.res.id + '/show/')
        }
      })
      .catch(err => {
        console.error('error')
      })
  }

  render() {
    return (
      <FeatureForm
        isNew
        data={{}}
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
