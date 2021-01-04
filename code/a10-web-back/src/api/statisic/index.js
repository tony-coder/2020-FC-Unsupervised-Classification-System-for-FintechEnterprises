import request from '@/utils/request'

export function getchartdata(data) {
  return request({
    url: '/api/bfx/statistic/chart',
    method: 'post',
    data
  })
}
export function getbardata() {
  return request({
    url: '/api/bfx/statistic/bar',
    method: 'get'
  })
}

