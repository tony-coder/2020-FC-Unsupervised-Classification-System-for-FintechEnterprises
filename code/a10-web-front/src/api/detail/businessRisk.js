import request from '@/utils/request'

// 处罚
export function punishmentFind(data) {
  return request({
    url: '/api/bfx/info/punishment',
    method: 'post',
    data
  })
}

// 欠款
export function overdraftFind(data) {
  return request({
    url: '/api/bfx/info/overdraft',
    method: 'post',
    data
  })
}

// 司法纠纷
export function judicialDisputeFind(data) {
  return request({
    url: '/api/bfx/info/judicialDispute',
    method: 'post',
    data
  })
}

export default {
  punishmentFind,
  overdraftFind,
  judicialDisputeFind
}
