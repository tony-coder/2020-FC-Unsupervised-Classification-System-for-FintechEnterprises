import request from '@/utils/request'

export function get2dcluster() {
  return request({
    url: '/api/bfx/statistic/2Dcluster',
    method: 'post'
  })
}
export function get3dcluster() {
  return request({
    url: '/api/bfx/statistic/3Dcluster',
    method: 'post'
  })
}
