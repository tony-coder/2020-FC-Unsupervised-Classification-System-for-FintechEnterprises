// 验证码模型
const captcha = {
  state: {
    expire: false,
    tcaptcha: false
  },
  mutations: {
    SET_EXPIRE: (state, expire) => {
      state.expire = expire
    },
    SET_TCAPTCHA: (state, tcaptcha) => {
      state.tcaptcha = tcaptcha
    }
  },
  actions: {
    validCode({ commit, state }, code) {
    //   return new Promise((resolve, reject) => {
    //     oneTime(code).then(response => {
    //       if (response) {
    //         commit('SET_TOKEN', response)
    //         resolve(response)
    //       } else {
    //         reject()
    //       }
    //     }).catch(error => {
    //       reject(error)
    //     })
    //   })
    },
    Expire({
      commit,
      state
    }, expire) {
      commit('SET_EXPIRE', expire)
    },
    Tcaptcha({
      commit,
      state
    }, tcaptcha) {
      commit('SET_TCAPTCHA', tcaptcha)
    }
  }
}

export default captcha
