import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import actions from '../../../actions'
import * as modelzooActions from '../modelzoo.actions'
import { formatDate, formatTime, formatAge } from '../../../util'
import { history } from '../../../store'
import { Loader, TableObject, Swatch } from '../../../common'
import ModelDownloadButton from '../components/modelDownload.button'

import ReactMarkdown from 'react-markdown'

class ModelZooShow extends Component {
  componentDidMount() {
    console.log(this.props.match.params.id)
    actions.modelzoo.show('name/' + this.props.match.params.id)
  }

  componentDidUpdate(prevProps){
    if (this.props.modelzoo.show.res
    && this.props.modelzoo.show !== prevProps.modelzoo.show
    && this.props.modelzoo.show.res.modelzoo_files) {
      const key = this.props.match.params.id
      const { res } = this.props.modelzoo.show
      this.props.modelzooActions.fetchModelZooFiles(key, res.modelzoo_files)
    }
  }

  render() {
    const { show, assets, images } = this.props.modelzoo
    const { id } = this.props.match.params
    if (show.loading) {
      return <Loader />
    }
    if (!show.loading && !show.res || show.not_found) {
      return <div className='gray'>Model {id} not found</div>
    }
    const { res: data } = show
    // console.log(data)
    const {
      name, task_type, framework, features,
      active, downloaded, tested, notes,
      model, labels, config,
      width, height, scale, mean, threshold,
      dimensions,
      rgb, crop,
      ...rest
    } = data
    const {
      'index.md': index_md,
      'license.md': license_md,
      ...otherAssets,
    } = assets

    return (
      <div className='modelzooShow'>
        <h1>{name}</h1>
        <div className='images'>
          {Object.keys(images).map(url => (
            <img src={url} key={url} />
          ))}
        </div>
        <Asset url={'index.md'} data={index_md} noTitle style="index_md" />
        {Object.keys(otherAssets).sort().map(url => (
          <Asset key={url} url={url} data={assets[url]} />
        ))}
        {!downloaded && (
            <ModelDownloadButton id={id} />
          )}
        <TableObject
          tag="Overview"
          order={"id name task_type framework features dimensions active downloaded tested".split(" ")}
          object={{
            id,
            name, task_type: task_type.replace(/_/g, " "), framework,
            features: (features || "Features missing"),
            dimensions: (dimensions ? dimensions + '-d feature vector' : "Dimensionality missing"),
            active: !!active,
            downloaded: !!downloaded,
            tested: !!tested,
          }}
        />
        <TableObject
          tag="Paths"
          order={"model labels config".split(" ")}
          object={{
            model, labels, config,
          }}
        />
        <TableObject
          tag="Image"
          order={"width height scale threshold mean rgb crop notes".split(" ")}
          object={{
            width, height,
            scale,
            rgb,
            crop,
            mean: { _raw: true, value: <Swatch color={data.mean} /> },
            threshold,
            notes,
          }}
        />
        <Asset url={'license.md'} data={license_md} noTitle style={'license'} />
      </div>
    )
  }
}

const Asset = ({ url, data, title, style, noTitle }) => {
  if (!data) return null
  let content;
  if (data.match(/----[-]+/)) {
    const partz = data.split(/----[-]+/)
    content = partz.slice(2).join('----')
  } else {
    content = data
  }
  return (
    <div className={style || 'asset'}>
      {!noTitle && <h3>{title || url}</h3>}
      <ReactMarkdown
        source={content}
        renderers={markdownRenderers}
      />
    </div>
  )
}
const markdownRenderers = {
  'link': props => {
    return <a href={props.href} target="_blank" rel="nofollow noopener noreferrer">{props.children}</a>
  }
}

/*
        <div className='buttons'>
          <Link to={"/feature/" + this.props.match.params.id + '/edit/'}>
            <button>Edit Feature</button>
          </Link>
          <button onClick={this.handleDestroy.bind(this)}>Delete Feature</button>
        </div>
*/

const mapStateToProps = state => ({
  modelzoo: state.modelzoo,
})

const mapDispatchToProps = dispatch => ({
  modelzooActions: bindActionCreators({ ...modelzooActions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(ModelZooShow)
