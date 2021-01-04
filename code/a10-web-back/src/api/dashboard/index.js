import request from '@/utils/request'

export function getinitdata() {
  return request({
    url: '/api/bfx/statistic/quantity',
    method: 'get'
  })
}

