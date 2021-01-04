import request from '@/utils/request'

export function uploadTrainData() {
  return request({
    url: '/api/bfx/statistic/uploadTrainData',
    method: 'post'
  })
}

export function stratTrain() {
  return request({
    url: '/api/bfx/statistic/trainModel',
    method: 'post'
  })
}

