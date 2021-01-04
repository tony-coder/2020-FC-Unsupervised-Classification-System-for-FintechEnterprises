import request from '@/utils/request'

// 登录
export function login(data) {
  return request({
    url: '/api/bfx/login',
    method: 'post',
    data
  })
}

// 注册
export function register(data) {
  return request({
    url: '/api/bfx/register',
    method: 'post',
    data
  })
}

export default{
  login,
  register
}
