import request from '@/utils/request'

// 工商信息
export function searchBasicInfo(data) {
  return request({
    url: '/api/bfx/info/basic',
    method: 'post',
    data
  })
}
// 自身风险
export function searchSelfRisk(data) {
  return request({
    url: '/api/bfx/info/selfRisk',
    method: 'post',
    data
  })
}

// 标签信息
export function searchTagInfo(data) {
  return request({
    url: '/api/bfx/info/tag',
    method: 'post',
    data
  })
}

// 对比企业信息
export function searchCompareEntInfo(data) {
  return request({
    url: '/api/bfx/info/compareEnt',
    method: 'post',
    data
  })
}

// 获取企业报告pdf地址
export function searchEntReporturl(data) {
  return request({
    url: '/api/bfx/info/reporturl',
    method: 'post',
    data
  })
}

export default {
  searchBasicInfo,
  searchSelfRisk,
  searchTagInfo,
  searchCompareEntInfo,
  searchEntReporturl
}
