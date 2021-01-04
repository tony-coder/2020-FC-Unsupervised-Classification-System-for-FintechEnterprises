import request from '@/utils/request'

// 招聘数据
export function searchRecruitInfo(data) {
  return request({
    url: '/api/bfx/info/recruit',
    method: 'post',
    data
  })
}

export default {
  searchRecruitInfo
}
