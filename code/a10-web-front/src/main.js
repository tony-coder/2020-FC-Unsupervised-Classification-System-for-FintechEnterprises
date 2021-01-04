// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
// 导入 Vue 框架
import Vue from 'vue'
// normalize.css是一种现代的、为HTML5准备的优质替代方案
import 'normalize.css/normalize.css'// A modern alternative to CSS resets
// 导入element-ui
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// import locale from 'element-ui/lib/locale/lang/en' // lang i18n
import '@/styles/index.scss' // global css
import '@/styles/common.scss' // global css
import '@/assets/iconfont/iconfont.css' // Iconfont-阿里巴巴矢量图标库

// 导入 app.vue 组件
import App from './App'
import router from './router'
import store from './store'

import * as filters from './filters' // global filters

Vue.config.productionTip = false

// 完整引入 Element size设为 medium
Vue.use(ElementUI, { size: 'medium' })

// 注册全局过滤器
Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key])
})

/* eslint-disable no-new */
// 创建 Vue 根实例
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
