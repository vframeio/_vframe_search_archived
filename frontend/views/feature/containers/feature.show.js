import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import actions from '../../../actions'
import * as featureActions from '../feature.actions'
import { formatDate, formatTime, formatAge } from '../../../util'
import { history } from '../../../store'
import { Loader, TableObject, Swatch } from '../../../common'

import ReactMarkdown from 'react-markdown'

const IndexNames = { 'flat': 'Flat', 'faiss': 'Faiss', 'annoy': 'Annoy' }

class FeatureShow extends Component {
  componentDidMount() {
    actions.feature.show(this.props.match.params.id)
  }

  componentDidUpdate(prevProps){
    if (this.props.feature.show !== prevProps.feature.show) {
      // onshow
    }
  }

  render() {
    const { index: modelzoo } = this.props.modelzoo
    const { show, assets, images } = this.props.feature
    if (show.loading || modelzoo.loading) {
      return <Loader />
    }
    if (!show.loading && !show.res || show.not_found) {
      return <div className='gray'>Model {this.props.match.params.id} not found</div>
    }
    const { res: data } = show
    console.log(data.process_id)

    return (
      <div className='featureShow'>
        <h1>{modelzoo.lookup[data.modelzoo_name].name}</h1>
        <TableObject
          order={"active model index_type created_at processed_at processed_to_id indexed_at indexed_to_id".split(" ")}
          object={{
            model: { _raw: true, value: <Link to={"/modelzoo/" + data.modelzoo_name + "/show/"}>{modelzoo.lookup[data.modelzoo_name].name}</Link> },
            active: data.active,
            created_at: data.created_at,
            processed_at: data.processed_at || "No feature vectors processed",
            processed_to_id: data.process_id ? { _raw: true, value: <Link to={"/media/id/" + data.process_id + "/show/"}>{data.process_id}</Link> } : 'n/a',
            indexed_at: data.indexed_at || "Not indexed",
            indexed_to_id: data.index_id ? { _raw: true, value: <Link to={"/media/id/" + data.index_id + "/show/"}>{data.index_id}</Link> } : 'n/a',
            index_type: IndexNames[data.index_type],
          }}
        />
      </div>
    )
    // index_settings
  }
}

const mapStateToProps = state => ({
  feature: state.feature,
  modelzoo: state.modelzoo,
})

const mapDispatchToProps = dispatch => ({
  featureActions: bindActionCreators({ ...featureActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(FeatureShow)
