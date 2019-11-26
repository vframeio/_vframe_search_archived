import React, { Component } from 'react'
import { Link } from 'react-router-dom'

import { session } from '../../../session'

import { TextInput, TextArea, Checkbox, Select, SubmitButton, Loader } from '../../../common'

const newFeature = () => ({
  modelzoo_name: "",
  index_type: "flat",
  username: session('username'),
  active: true,
  index_settings: "{}",
})

const indexTypes = [
  { name: "flat", label: "Flat" },
  { name: "annoy", label: "Annoy" },
  { name: "faiss", label: "FAISS" }
]

export default class FeatureForm extends Component {
  state = {
    title: "",
    submitTitle: "",
    data: { ...newFeature() },
    errorFields: new Set([]),
    modelzooNames: [],
  }

  componentDidMount() {
    const { data, isNew } = this.props
    const title = isNew ? 'New Feature' : 'Editing Feature #' + data.id
    const submitTitle = isNew ? "Create Feature" : "Save Changes"
    const modelzooNames = this.getModelZooNames()
    this.setState({
      title,
      submitTitle,
      modelzooNames,
      errorFields: new Set([]),
      data: { 
        ...newFeature(),
        ...data
      },
    })
  }

  componentDidUpdate(prevProps) {
    if (this.props.modelzoo.index !== prevProps.modelzoo.index) {
      const modelzooNames = this.getModelZooNames()
      this.setState({
        modelzooNames
      })
    }
  }

  getModelZooNames() {
    const { lookup, order } = this.props.modelzoo.index
    return order ? order.map(name => {
      const { name: label, active, downloaded } = lookup[name]
      if (active && downloaded) {
        return { name, label }
      }
      return null
    }).filter(x => !!x) : []
  }

  handleChange(e) {
    const { errorFields } = this.state
    const { name, value } = e.target
    if (errorFields.has(name)) {
      errorFields.delete(name)
    }
    this.setState({
      errorFields,
      data: {
        ...this.state.data,
        [name]: value,
      }
    })
  }

  handleSelect(name, value) {
    const { errorFields } = this.state
    if (errorFields.has(name)) {
      errorFields.delete(name)
    }
    this.setState({
      errorFields,
      data: {
        ...this.state.data,
        [name]: value,
      }
    })
  }


  handleSubmit(e) {
    e.preventDefault()
    const { isNew, onSubmit } = this.props
    const { data } = this.state
    // const requiredKeys = "title username".split(" ")
    const requiredKeys = "modelzoo_name index_type active".split(" ")
    const validKeys = "modelzoo_name index_type active".split(" ")
    const validData = validKeys.reduce((a,b) => { a[b] = data[b]; return a }, {})
    const errorFields = requiredKeys.filter(key => !validData[key])
    if (errorFields.length) {
      console.log('error', errorFields, validData)
      this.setState({ errorFields: new Set(errorFields) })
    } else {
      if (isNew) {
        session.set('username', data.username)
      } else {
        validData.id = data.id
      }
      console.log('submit', validData)
      onSubmit(validData)
    }
  }

  render() {
    const { isNew } = this.props
    const { title, submitTitle, errorFields, data, modelzooNames } = this.state
    return (
      <div className='form'>
        <h1>{title}</h1>
        <form onSubmit={this.handleSubmit.bind(this)}>
          <Select
            name="modelzoo_name"
            required
            className='wide'
            title={"ModelZoo Name"}
            defaultOption={'Select a model'}
            selected={data.modelzoo_name}
            options={modelzooNames}
            onChange={this.handleSelect.bind(this)}
          />
          <Select
            name="index_type"
            required
            title={"Index Type"}
            selected={data.index_type}
            options={indexTypes}
            onChange={this.handleSelect.bind(this)}
          />
          <Checkbox
            name="active"
            label="Active"
            checked={data.active}
            onChange={this.handleChange.bind(this)}
          />
          <SubmitButton
            title={submitTitle}
            onClick={this.handleSubmit.bind(this)}
          />
          {!!errorFields.size &&
            <label>
              <span></span>
              <span>Please complete the required fields =)</span>
            </label>
          }
        </form>
      </div>
    )
  }
}
