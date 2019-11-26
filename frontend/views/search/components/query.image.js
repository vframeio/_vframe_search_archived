import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { clamp, percent } from '../../../util'

export default class QueryImage extends Component {
  render() {
    const { query, infer } = this.props
    const media = query.media || query.upload
    if (!media || !media.url) {
      return <div className='queryImage' />
    }
    const detections = (infer.detections || []).map(({ label, rect }, i) => {
      return (
        <div
        className='rect'
          key={i}
          style={{
            left: percent(clamp(rect.x1)),
            width: percent(clamp(rect.x2 - rect.x1, 0, Math.min(1.0, 1.0 - rect.x1))),
            top: percent(clamp(rect.y1)),
            height: percent(clamp(rect.y2 - rect.y1, 0, Math.min(1.0, 1.0 - rect.y1))),
          }}>
          <span>{label.replace(/_/g, ' ')}</span>
        </div>
      )
    })
    return (
      <div className='queryImage'>
        <div className='querySelector'>
          <img src={media.url} />
          {detections}
        </div>
        <div className='uploadText'>
          Image processed in {query.timing.toFixed(2)} seconds
        </div>
      </div>
    )
  }
}
