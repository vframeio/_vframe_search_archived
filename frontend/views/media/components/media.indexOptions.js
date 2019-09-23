import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import actions from '../../../actions'

import { Select, Checkbox } from '../../../common'

const thumbnailOptions = [
  { name: 'th', label: 'Thumbnails', },
  { name: 'sm', label: 'Small', },
  { name: 'md', label: 'Medium', },
  { name: 'lg', label: 'Large', },
  { name: 'orig', label: 'Original', },
]

const sortOptions = [
  { name: 'id-asc', label: 'Most recent' },
  { name: 'id-desc', label: 'Oldest first' },
  // { name: '-asc', label: '' },
  // { name: '-desc', label: '' },
  // { name: '-asc', label: '' },
  // { name: '-desc', label: '' },
  // { name: '-asc', label: '' },
  // { name: '-desc', label: '' },
]

class IndexOptions extends Component {
  render() {
    const { options, searchOptions } = this.props
    return (
      <div className='row menubar'>
        <div />
        <Select
          name={'sort'}
          options={sortOptions}
          selected={options.sort}
          onChange={actions.media.updateOption}
        />
        <Select
          name={'thumbnailSize'}
          options={thumbnailOptions}
          selected={searchOptions.thumbnailSize}
          onChange={actions.search.updateOption}
        />
      </div>
    )
  }
}

const mapStateToProps = state => ({
  options: state.media.options,
  searchOptions: state.search.options,
})

const mapDispatchToProps = dispatch => ({
})

export default connect(mapStateToProps, mapDispatchToProps)(IndexOptions)
