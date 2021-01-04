import request from '@/utils/request'

export function getresultData(data) {
  return request({
    url: '/api/bfx/test/predict',
    method: 'post',
    data
  })
}

export function stratTrain() {
  return request({
    url: '/api/bfx/test/train',
    method: 'get'
  })
}

