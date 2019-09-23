import React, { Component } from 'react'
// import { Link } from 'react-router-dom'

import { Select, Checkbox } from '../../../common'
import FeatureSelect from '../../feature/components/feature.select.js'

export default class QueryOptions extends Component {
  updateOption(name, value) {
    this.props.searchActions.updateOption(name, value)
  }

  handleSubmit() {
  }

  render() {
    const { options, info, query, feature, modelzoo } = this.props
    const log = [
      'Analyzing results using COCO objects model "coco_model.caffemodel"',
      "Comparing results to 56,013 images...",
      "Generating visualization...",
      "Analysis took 1.3 seconds",
    ]

    return (
      <div className='queryOptions'>
        <div className='row'>
          <FeatureSelect />
          <button
            className='process'
            disabled={!query.url}
            onClick={this.handleSubmit.bind(this)}
          >
            Process
          </button>
        </div>

        <div className='row'>
          <Checkbox
            name="autoprocess"
            label="Auto-Process"
            checked={options.autoprocess}
            onChange={this.updateOption.bind(this)}
          />
          <Checkbox
            name="visualization"
            label="Create Visualization"
            checked={options.visualization}
            onChange={this.updateOption.bind(this)}
          />
        </div>
        <div className='row'>
          <Checkbox
            name="jitter"
            label="Jitter"
            checked={options.jitter}
            onChange={this.updateOption.bind(this)}
          />
          <Checkbox
            name="verbose"
            label="Verbose"
            checked={options.verbose}
            onChange={this.updateOption.bind(this)}
          />
        </div>

        {this.props.query.crop &&
          <div>
            <img src="/static/img/demo-crop.png" className='preview' />
          </div>
        }

        {this.props.infer && this.props.infer.classifications && !!this.props.infer.classifications.length &&
          <div className='classifications'>
            <h4>Found these objects:</h4>
            {this.props.infer.classifications.map(c => <div key={c.label}>{c.label}</div>)}
          </div>
        }

        {this.props.query.log &&
          <div className='log'>
            {log.map(s => <span key={s}>{s}</span>)}
          </div>
        }
      </div>
    )
  }
}
