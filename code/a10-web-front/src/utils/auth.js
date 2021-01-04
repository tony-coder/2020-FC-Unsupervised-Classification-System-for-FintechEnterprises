import Cookies from 'js-cookie'

const TokenKey = 'Authorization'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token, {
    expires: ''
  })
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

const CodeKey = 'code'
export function getCode() {
  return Cookies.get(CodeKey)
}

export function setCode(token) {
  return Cookies.set(CodeKey, token, {
    expires: ''
  })
}

export function removeCode() {
  return Cookies.remove(CodeKey)
}
