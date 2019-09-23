def IndexFactory(feature):
  if feature.index_type == 'annoy':
    from app.indexes.annoy_index import AnnoyIndex
    return AnnoyIndex(feature)
  if feature.index_type == 'faiss':
    from app.indexes.faiss_index import FaissIndex
    return FaissIndex(feature)
  if feature.index_type == 'flat':
    from app.indexes.flat_index import FlatIndex
    return FlatIndex(feature)
