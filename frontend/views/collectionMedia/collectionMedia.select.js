import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import { session } from '../../session'
import { Select, SmallMenuButton } from '../../common'
import actions from '../../actions'

const loadingOptions = [{ name: 'loading', label: 'Loading collections...' }]

export class CollectionMediaSelect extends Component {
  state = {
    loading: true,
    options: loadingOptions,
  }

  componentDidMount() {
    actions.collection.index()
  }

  componentDidUpdate(prevProps, props) {
    const { collection } = this.props
    const diff = ['collection'].some(s => this.props[s] !== prevProps[s])
    const loading = !!(
      collection.loading || !collection.order
    )
    if (diff && !loading && this.state.options === loadingOptions) {
      const options = collection.order
        .map(id => collection.lookup[id])
        .filter(el => !el.archived)
        .map(el => ({
          name: el.id,
          label: el.title,
        }))
      if (!session.get('currentCollection') && collection.lookup.length) {
        session.set('currentCollection', collection.lookup[0].id)
      }
      this.setState({ loading, options })
    }
  }

  changeFeature(name, value) {
    actions.collectionMedia.load(value)
  }

  render() {
    const { collectionMedia } = this.props
    const { loading, options } = this.state
    // console.log(options, session.get('currentCollection'))
    return (
      <div className='row center collectionSelectContainer'>
        <Select
          name='currentFeature'
          options={options}
          loading={loading}
          className='collectionSelect'
          defaultOption={'Select a collection'}
          selected={parseInt(collectionMedia.id)}
          onChange={this.changeFeature.bind(this)}
        />
        <SmallMenuButton name='open_in_new' label={false} href={'/collection/' + collectionMedia.id + '/show/'} />
      </div>
    )
  }
}

const mapStateToProps = state => ({
  collection: state.collection.index,
  collectionMedia: state.collectionMedia,
})

const mapDispatchToProps = dispatch => ({
  // actions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(CollectionMediaSelect)
