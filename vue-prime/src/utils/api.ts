export async function fetch_api_att2font(path: string = '', picture: boolean) {
  const response = await fetch(`http://127.0.0.1:5000/api${path}`, {
    method: 'GET'
  })
  if (picture) {
    const blob = await response.blob()
    return URL.createObjectURL(blob)
  } else return await response.json()
}
export async function fetch_api_Logo(path: string = '', picture: boolean) {
  const response = await fetch(`http://127.0.0.1:8000/api${path}`, {
    method: 'GET'
  })
  if (picture) {
    const blob = await response.blob()
    return URL.createObjectURL(blob)
  } else return await response.json()
}
export async function post_api_att2font(path: string = '', data: object) {
  const response = await fetch(`http://127.0.0.1:5000/api${path}`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  return await response.json()
}
export async function post_api_Logo(path: string = '', data: string) {
  const response = await fetch(`http://127.0.0.1:8000/api${path}`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  return await response.json()
}
