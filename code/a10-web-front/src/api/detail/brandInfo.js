import request from '@/utils/request'

// 知识产权数据
export function searchBrandInfo(data) {
  return request({
    url: '/api/bfx/info/brand',
    method: 'post',
    data
  })
}

export default {
  searchBrandInfo
}
