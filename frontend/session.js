import Storage from 'store2'

export const session = Storage.namespace('vcat.search')

export const getDefault = (key, def) => {
  const val = session.get(key);
  return (val === null) ? def : val
}
export const getDefaultInt = (key, def) => {
  return parseInt(getDefault(key, def), 10)
}
export const getDefaultFloat = (key, def) => {
  return parseFloat(getDefault(key, def), 10)
}

const username = session.get('username')
if (!username) {
  session.set('username', 'anonymous')
}
