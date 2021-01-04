import request from '@/utils/request'

// 推荐企业
const searchRecommandEnt = function(data) {
  return request({
    url: '/api/bfx/info/recommend',
    method: 'post',
    data
  })
}

export default{
  searchRecommandEnt
}
