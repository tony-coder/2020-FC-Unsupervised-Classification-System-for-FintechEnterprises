import request from '@/utils/request'

// 知识产权数据
export function searchIntellectualPropertyInfo(data) {
  return request({
    url: '/api/bfx/info/intellectualProperty',
    method: 'post',
    data
  })
}

export default {
  searchIntellectualPropertyInfo
}
