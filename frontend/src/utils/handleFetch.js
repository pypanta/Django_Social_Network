async function refreshToken() {
  try {
    const response = await fetch('http://localhost:8000/api/refresh/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      //body: {}
    })
    if (response.ok) {
      // const responseData = await response.json();

      // Set default header for every fetch() request
      // https://stackoverflow.com/questions/44820568/set-default-header-for-every-fetch-request
      //const oldFetch = window.fetch
      //window.fetch = function() {
      //  arguments[1].headers = { 'Authorization' : `Bearer ${responseData.access}` }
      //  return oldFetch.apply(window, arguments)
      //}

      return response;
    } else {
      throw response;
    }
  } catch(error) {
    return error;
  }
}

async function fetchData(end_point, method=null, data=null) {
  let jsonData = null;
  if (data) {
    jsonData = JSON.stringify(data);
  }

  const url = `http://localhost:8000/api/${end_point}/`

  try {
    const response = await fetch(url, {
      method: method,
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: jsonData
    })
    if (response.status === 200) {
      return response;
    } else if (response.status === 401 && end_point !== 'login') {
      const respRefreshToken = await refreshToken();
      if (respRefreshToken.ok) {
        const res = await fetchData(end_point, method, data)
        return res
      } else {
        throw respRefreshToken;
      }
    } else {
      throw response;
    }
  } catch(error) {
    return error;
  }
}

export default fetchData;
