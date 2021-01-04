import request from '@/utils/request'

// 推荐企业
export function searchInvestmentInfo(data) {
  return request({
    url: '/api/bfx/info/investment',
    method: 'post',
    data
  })
}

export default {
  searchInvestmentInfo
}
