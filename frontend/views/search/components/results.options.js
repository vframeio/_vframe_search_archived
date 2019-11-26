import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import * as searchActions from '../search.actions'

import { Select, Checkbox, MenuButton } from '../../../common'
import CollectionMediaSelect from '../../collectionMedia/collectionMedia.select'

const thumbnailOptions = [
  { name: 'th', label: 'Thumbnails', },
  { name: 'sm', label: 'Small', },
  { name: 'md', label: 'Medium', },
  { name: 'lg', label: 'Large', },
  { name: 'orig', label: 'Original', },
]

const sortOptions = [
  { name: 'score-asc', label: 'Score' },
  { name: 'date-asc', label: 'Most recent' },
  { name: 'date-desc', label: 'Oldest first' },
  { name: 'size-asc', label: 'Largest size' },
  { name: 'size-desc', label: 'Smallest size' },
  // { name: '-asc', label: '' },
  // { name: '-desc', label: '' },
  // { name: '-asc', label: '' },
  // { name: '-desc', label: '' },
  // { name: '-asc', label: '' },
  // { name: '-desc', label: '' },
]

class ResultsOptions extends Component {
  render() {
    const { options, actions } = this.props
    return (
      <div className='row menubar'>
        <div className='row'>
          <CollectionMediaSelect />
        </div>
        <Checkbox
          name='showGraphic'
          label='Hide graphic content'
          checked={options.showGraphic}
          onChange={actions.updateOption}
        />
        <Select
          name={'sort'}
          options={sortOptions}
          selected={options.sort}
          onChange={actions.updateOption}
        />
        <Select
          name={'thumbnailSize'}
          options={thumbnailOptions}
          selected={options.thumbnailSize}
          onChange={actions.updateOption}
        />
      </div>
    )
  }
}

const mapStateToProps = state => ({
  query: state.search.query.query,
  results: state.search.query.results,
  options: state.search.options,
})

const mapDispatchToProps = dispatch => ({
  actions: bindActionCreators({ ...searchActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(ResultsOptions)
