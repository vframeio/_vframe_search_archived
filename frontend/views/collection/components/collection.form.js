import React, { Component } from 'react'
import { Link } from 'react-router-dom'

import { session } from '../../../session'

import { TextInput, TextArea, Checkbox, SubmitButton, Loader } from '../../../common'

const newCollection = () => ({
  title: '',
  username: session('username'),
  notes: '',
  archived: false,
})

export default class CollectionForm extends Component {
  state = {
    title: "",
    submitTitle: "",
    data: { ...newCollection() },
    errorFields: new Set([]),
  }

  componentDidMount() {
    const { data, isNew } = this.props
    const title = isNew ? 'New Collection' : 'Editing ' + data.title
    const submitTitle = isNew ? "Create Collection" : "Save Changes"
    this.setState({
      title,
      submitTitle,
      errorFields: new Set([]),
      data: { 
        ...newCollection(),
        ...data
      },
    })
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

  handleSubmit(e) {
    e.preventDefault()
    const { isNew, onSubmit } = this.props
    const { data } = this.state
    const requiredKeys = "title username".split(" ")
    const validKeys = "title username notes archived".split(" ")
    const validData = validKeys.reduce((a,b) => { a[b] = data[b]; return a }, {})
    const errorFields = requiredKeys.filter(key => !validData[key])
    if (errorFields.length) {
      console.log('error', errorFields, validData)
      this.setState({ errorFields: new Set(errorFields) })
    } else {
      if (isNew) {
        // side effect: set username if we're creating a new collection
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
    const { title, submitTitle, errorFields, data } = this.state
    return (
      <div className='form'>
        <h1>{title}</h1>
        <form onSubmit={this.handleSubmit.bind(this)}>
          <TextInput
            title="Title"
            name="title"
            required
            data={data}
            error={errorFields.has('title')}
            onChange={this.handleChange.bind(this)}
          />
          <TextInput
            title="Author"
            name="username"
            required
            data={data}
            error={errorFields.has('username')}
            onChange={this.handleChange.bind(this)}
          />
          <TextArea
            title="Notes"
            name="notes"
            data={data}
            onChange={this.handleChange.bind(this)}
          />
          {!isNew &&
            <Checkbox
              name="archived"
              label="Archived"
              checked={data.archived}
              onChange={this.handleChange.bind(this)}
            />
          }
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
