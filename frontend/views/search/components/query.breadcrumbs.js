import React, { Component } from 'react'
import { Link } from 'react-router-dom'

export default class QueryBreadcrumbs extends Component {
  render() {
    const collectionCount = 12
    const uploadCount = 34
    const filename = 'file-001-abcd.jpg'
    const breadcrumbs = [
      <Link key={'root'} to="/collection/">{'Collections (' + collectionCount + ')'}</Link>,
      ' / ',
      <Link key={'collection'} to="/uploads/">{'Uploads (' + uploadCount + ')'}</Link>,
      ' / ',
      filename,
    ]
    return (
      <div className='breadcrumbs'>
        {breadcrumbs}
      </div>
    )
  }
}
