import request from '@/utils/request'

// 知识产权数据
export function searchCreditInfo(data) {
  return request({
    url: '/api/bfx/info/credit',
    method: 'post',
    data
  })
}

export default {
  searchCreditInfo
}
