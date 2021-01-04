import request from '@/utils/request'

export function retrain(data) {
  return request({
    url: '/api/bfx/statistic/modelParam',
    method: 'post',
    data
  })
}
export function getModelParam() {
  return request({
    url: '/api/bfx/statistic/modelParam',
    method: 'get'
  })
}

