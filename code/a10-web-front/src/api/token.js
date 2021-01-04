/**
 * token 相关接口
 */
import request from '@/utils/request'

/**
 * 校验验证码，获取token
 */
export function tcapatcha(data) {
  return request({
    url: '/api/auth/jwt/tcapatcha',
    method: 'post',
    data
  })
}

/**
 * 校验验证码，获取token
 */
export function oneTime(code) {
  return request({
    url: '/api/auth/jwt/oneTime',
    method: 'post',
    data: {
      code
    }
  })
}

/**
 * 校验token
 */
export function verify(token) {
  return request({
    url: '/api/auth/jwt/verify',
    method: 'get',
    params: {
      token
    }
  })
}
