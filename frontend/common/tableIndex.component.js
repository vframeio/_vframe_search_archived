import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'

import { formatDateTime } from '../util'
import { Loader, Swatch, Dot } from '../common'

/*
  <TableIndex
    title="Collections"
    actions={actions.collection}
    data={data.collection.index}
    fields={[
      { name: 'title', type: 'title', link: row => '/collection/' + row.id + '/show/' },
      { name: 'username', type: 'string' },
      { name: 'date', type: 'date' },
      { name: 'notes', type: 'text' },
    ]}
  />
*/

export default class TableIndex extends Component {
  componentDidMount() {
    this.props.actions && this.props.actions.index()
  }

  render() {
    const { data, els, title, fields, noHeadings, notFoundMessage } = this.props
    if (data.loading) {
      return <Loader />
    }
    if (!els && (!data.lookup || !data.order.length)) {
      return (
        <div>
          <h1>{title}</h1>
          <p className='gray'>
            {notFoundMessage || ("No " + title)}
          </p>
        </div>
      )
    }
    return (
      <div>
        <h1>{title}</h1>
        <div className='rows'>
        {!noHeadings && <RowHeadings fields={fields} />}
        {els
          ? els.map(el => <Row key={el.id} row={el} fields={fields} />)
          : data.order.map(id => <Row key={id} row={data.lookup[id]} fields={fields} />)
        }
        </div>
      </div>
    )
  }
}

const RowHeadings = ({fields}) => {
  return (
    <div className='row heading'>
      {fields.map(field => {
        let css = {}
        if (field.width) {
          css = { width: field.width, maxWidth: 'none', flex: 'none', }
        }
        if (field.flex) {
          css.flex = field.flex
        }
        return <div key={field.name} className={field.type} style={css}>{(field.title || field.name).replace(/_/g, ' ')}</div>
      })}
    </div>
  )
}

const Row = ({ row, fields }) => {
  return (
    <div className='row'>
      {fields.map(field => {
        let value = field.valueFn ? field.valueFn(row) : row[field.name]
        let css = {}
        if (field.type === 'date' && (row.updated_at || row.created_at || value)) {
          // value = (value || "").split('.')[0]
          value = formatDateTime(row.updated_at || row.created_at || value)
        } else if (field.type === 'text') {
          value = String(value || "").trim().split('\n')[0].replace(/^#+/, '').substr(0, 100)          
        } else if (field.type === 'color') {
          value = <Swatch color={value} />
        } else if (field.type === 'bool') {
          value = <Dot color={value ? '#11f' : '#fff'} />
        } else if (field.type === 'str') {
          value = String(value || "").replace(/_/g, ' ')
        }
        if (field.width) {
          css = { width: field.width, maxWidth: 'none', flex: 'none', }
        }
        if (field.flex) {
          css.flex = field.flex
        }
        let className
        if (field.style) {
          className = field.type + ' ' + field.style
        } else {
          className = field.type
        }
        value = <div title={value} key={field.name} className={className} style={css}>{value}</div>
        if (field.link) {
          return <Link key={field.name} to={field.link(row)}>{value}</Link>
        }
        return value
      })}
    </div>
  )
}
