import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/api/bfx/user/login',
    method: 'post',
    data,
    headers: {
      'connection': 'keep-alive',
      'Content-Type': 'application/json'
    }
  })
}

export function getInfo(token) {
  return request({
    url: '/api/bfx/user/info',
    method: 'get',
    params: { token },
    headers: {
      'connection': 'keep-alive',
      'Authorization': 'TOKEN ' + token
    }
  })
}

export function logout() {
  return request({
    url: '/api/bfx/user/logout',
    method: 'post'
  })
}
