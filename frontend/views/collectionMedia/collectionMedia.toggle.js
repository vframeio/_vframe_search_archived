import React, { Component } from 'react'
import { SmallMenuButton } from '../../common'

import actions from '../../actions'

export default class CollectionMediaToggle extends Component {
  render() {
    const { collectionMedia, id } = this.props
    if (!collectionMedia || !collectionMedia.lookup) return null
    const active = collectionMedia.lookup.has(id)
    return (
      <SmallMenuButton
        name="new"
        onClick={() => (active
          ? actions.collectionMedia.remove_media(collectionMedia.id, id)
          : actions.collectionMedia.add_media(collectionMedia.id, id)
        )}
        active={active}
      />
    )
  }
}
