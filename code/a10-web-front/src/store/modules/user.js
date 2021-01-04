import {
  getToken,
  setToken,
  removeToken
} from '@/utils/auth'
import {
  verify,
  oneTime
} from '@/api/token'
import {
  login,
  register
} from '@/api/user'
// state：包含了store中存储的各个状态。
// getter: 类似于 Vue 中的计算属性，根据其他 getter 或 state 计算返回值。
// mutation: 一组方法，是改变store中状态的执行者，只能是同步操作。
// action: 一组方法，其中可以包含异步操作。
const user = {
  state: {
    token: getToken(),
    expire: false,
    tcaptcha: false
  },
  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token
      setToken(token)
    },
    SET_EXPIRE: (state, expire) => {
      state.expire = expire
    },
    SET_TCAPTCHA: (state, tcaptcha) => {
      state.tcaptcha = tcaptcha
    }
  },
  actions: {
    // 用户名密码登录
    Login({ commit }, userInfo) {
      const username = userInfo.username.trim()
      const password = userInfo.password.trim()
      const data = {
        username,
        password
      }
      return new Promise((resolve, reject) => {
        login(data).then(resp => {
          const data = resp.data
          console.log(resp.data)
          commit('SET_TOKEN', data.token)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },
    // 注册
    Register({ commit }, userInfo) {
      const username = userInfo.username.trim()
      const password = userInfo.password.trim()
      const data = {
        username,
        password
      }
      return new Promise((resolve, reject) => {
        register(data).then(resp => {
        //   const data = resp.data
        }).catch(error => {
          reject(error)
        })
      })
    },
    // 单点登录
    validCap({ commit, state }, token) {
      return new Promise((resolve, reject) => {
        verify(token).then(response => {
          commit('SET_TOKEN', token)
          resolve(response)
        }).catch(error => {
          reject(error)
        })
      })
    },
    validCode({ commit, state }, code) {
      return new Promise((resolve, reject) => {
        oneTime(code).then(response => {
          if (response) {
            commit('SET_TOKEN', response)
            resolve(response)
          } else {
            reject()
          }
        }).catch(error => {
          reject(error)
        })
      })
    },
    Expire({ commit, state }, expire) {
      commit('SET_EXPIRE', expire)
    },
    Tcaptcha({
      commit,
      state
    }, tcaptcha) {
      commit('SET_TCAPTCHA', tcaptcha)
    },
    // 前端 登出
    FedLogOut({
      commit
    }) {
      return new Promise(resolve => {
        commit('SET_TOKEN', '')
        removeToken()
        resolve()
      })
    }
  }
}

export default user
