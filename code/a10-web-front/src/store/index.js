import Vue from 'vue'
import Vuex from 'vuex'
import app from './modules/app'
import user from './modules/user'
import captcha from './modules/captcha'
import tagsView from './modules/tagsView'
import getters from './getters'

// 我们组装模块并导出 store 的地方

// vuex是专为vue.js应用程序开发的状态管理模式。它采用集中存储管理应用的所有组件的状态，并以相应的规则保证状态以一种可预测的方式发生变化。
// vuex也集成vue的官方调试工具devtools extension，提供了诸如零配置的time-travel调试、状态快照导入导出等高级调试功能。
Vue.use(Vuex)

// Vuex 主要有四部分：
// state：包含了store中存储的各个状态。
// getter: 类似于 Vue 中的计算属性，根据其他 getter 或 state 计算返回值。
// mutation: 一组方法，是改变store中状态的执行者，只能是同步操作。
// action: 一组方法，其中可以包含异步操作。

const store = new Vuex.Store({
  modules: {
    app,
    user,
    captcha,
    tagsView
  },
  getters
})

export default store
