import request from '@/utils/request'

// 搜索
export function search(data) {
  return request({
    url: '/api/bfx/search/',
    method: 'post',
    data
  })
}

// 获取热搜企业
export function searchHot() {
  return request({
    url: '/api/bfx/search/hot',
    method: 'get'
  })
}

export function searchTip(data) {
  return request({
    url: '/api/bfx/searchTip/',
    method: 'post',
    data
  })
}

export function searchRisk(data) {
  return request({
    url: '/api/bfx/search/risk/',
    method: 'post',
    data
  })
}

export function searchCluster(data) {
  return request({
    url: '/api/bfx/search/cluster',
    method: 'post',
    data
  })
}

// 批量查询文件上传
export function RequestUploads(formData) {
  return request({
    url: '/bfx/upload/',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data' // 文件上传
      // 'Content-Type': 'application/x-www-form-urlencoded',  // 表单
      // 'Content-Type': 'application/json;charset=UTF-8'  // json
    }
  })
}

export default{
  search,
  searchHot,
  searchTip,
  searchRisk,
  searchCluster
}
