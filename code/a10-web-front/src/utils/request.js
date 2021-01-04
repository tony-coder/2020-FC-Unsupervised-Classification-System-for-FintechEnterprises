import axios from 'axios'
// import Qs from 'qs'
import {
  Message,
  // MessageBox,
  Notification
} from 'element-ui'

import store from '../store'
import {
  getToken,
  removeToken
} from './auth'

// create an axios instance
const service = axios.create({
  // baseURL: process.env.BASE_API, // api的base_url
  timeout: 50000, // request timeout
  transformRequest: [function(data) {
    // 这里可以在发送请求之前对请求数据做处理，比如form-data格式化等，这里可以使用开头引入的Qs（这个模块在安装axios的时候就已经安装了，不需要另外安装）
    // JSON是正常类型的JSON
    data = JSON.stringify(data)
    // 由于使用的form-data传数据所以要格式化
    // if (!(data instanceof FormData)) {
    //   // qs.stringify()将对象 序列化成URL的形式，以&进行拼接
    //   data = Qs.stringify(data)
    // }
    return data
  }]
})

// request拦截器
service.interceptors.request.use(config => {
  // Do something before request is sent
  if (getToken()) {
    config.headers.Authorization = getToken() // 让每个请求携带token--['X-Token']为自定义key 请根据实际情况自行修改
  }
  config.headers['Need-Permission'] = false
  // config.headers['user-ip'] = window.returnCitySN['cip']
  return config
}, error => {
  // Do something with request error
  console.log(error) // for debug
  Promise.reject(error)
})

// respone拦截器
service.interceptors.response.use(
  response => {
    /**
     * 下面的注释为通过response自定义code来标示请求状态，当code返回如下情况为权限有问题，登出并返回到登录页
     * 如通过xmlhttprequest 状态码标识 逻辑可写在下面error中
     */
    const res = response.data
    // if (response.status === 401 || res.status === 40101) {}
    // if (res.status === 30101) {}
    if (res.status === 40102) { // token异常
      removeToken()
      console.error(res.message)
    }
    if (res.status === 40301) { // token异常
      store.dispatch('Expire', true)
      // location.href = '/'
    }

    if (response.status !== 200 && res.status !== 200) {
      Message({
        message: res.message,
        type: 'error',
        duration: 5 * 1000
      })
    } else {
      return response.data // 返回数据
    }
  },
  error => {
    console.log('err ' + error) // for debug
    const response = error.response
    if (response === undefined) {
      Message({
        message: '服务请求超时！',
        type: 'error',
        duration: 5 * 1000
      })
      return Promise.reject(error)
    }
    const info = response.data
    // 403
    if (response.status === 403) {
      Notification.warning({
        title: '禁止',
        message: info.message,
        type: 'error',
        duration: 2 * 1000
      })
      return Promise.reject(error)
    }
    // 504
    if (response.status === 504) {
      Message({
        message: '后端服务异常，请联系管理员！',
        type: 'error',
        duration: 5 * 1000
      })
      return Promise.reject(error)
    }
    // 500
    if (response.status === 500) {
      Message({
        message: '后端服务器错误！',
        type: 'error',
        duration: 5 * 1000
      })
      console.error(info.message)
      return Promise.reject(error)
    }
    console.error(error)
    // Message({
    //   message: info.message,
    //   type: 'error',
    //   duration: 5 * 1000
    // })
    return Promise.reject(error)
  }
)

export default service
