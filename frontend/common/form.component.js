import React, { Component } from 'react';

export const TextInput = props => (
  <label className={props.error ? 'error' : 'text'}>
    <span>{props.title}</span>
    <input
      type="text"
      required={props.required}
      onChange={props.onChange}
      name={props.name}
      value={props.data[props.name]}
    />
  </label>
)

export const TextArea = props => (
  <label className={props.error ? 'textarea error' : 'textarea'}>
    <span>{props.title}</span>
    <textarea
      onChange={props.onChange}
      name={props.name}
      value={props.data[props.name]}
    />
  </label>
)

export const Checkbox = props => (
  <label>
    <input
      type="checkbox"
      name={props.name}
      value={1}
      checked={props.checked}
      onChange={(e) => props.onChange(props.name, e.target.checked)}
    />
    <span>{props.label}</span>
  </label>
)

export class Select extends Component {
  state = {
    focused: false,
  }

  render() {
    const { name, selected, options, defaultOption, title, loading, onChange, className } = this.props
    if (loading) {
      return <label className='select'><div>Loading...</div></label>
    }
    const { focused } = this.state
    return (
      <label>
        {title && <span>{title}</span>}
        <div className={(focused ? 'select focus' : 'select') + " " + (className || "")}>
          <div>{(options.find(opt => opt.name === selected) || {label: defaultOption}).label}</div>
          <select
            onFocus={() => this.setState({ focused: true })}
            onBlur={() => this.setState({ focused: false })}
            onChange={e => {
              onChange(name, e.target.value)
              // this.setState({ focused: false })
            }}
            value={selected || "__default__"}
          >
            {!selected && defaultOption && <option value="__default__">{defaultOption}</option>}
            {options.map((option, i) => (
              <option key={option.name} value={option.name}>{option.label}</option>
            ))}
          </select>
        </div>
      </label>
    )
  }
}

export class FileInput extends Component {
  handleChange(e) {
    const files = e.dataTransfer ? e.dataTransfer.files : e.target.files
    let i
    let file
    for (i = 0; i < files.length; i++) {
      file = files[i]
      if (file && file.type.match('image.*')) break
    }
    if (!file) return
    this.props.onChange(file)
  }

  render() {
    return (
      <input type="file" onChange={this.handleChange.bind(this)} />
    )
  }
}

export const SubmitButton = (props) => (
  <label>
    <span></span>
    <button onClick={props.onClick}>{props.title}</button>
  </label>
)

export const Loader = () => (
  <div>
    <div className='circular-loader color'>
      <div className="stroke">
        <div className="stroke-left"></div>
        <div className="stroke-right"></div>
      </div>
    </div>
  </div>
)

export const Swatch = ({ color }) => (
  <div
    className='swatch'
    style={{ backgroundColor: color ? 'rgb(' + color.join(',') + ')' : 'transparent' }}
  />
)

export const Dot = ({ color }) => (
  <div
    className='dot'
    style={{ backgroundColor: color }}
  />
)