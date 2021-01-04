import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'

Vue.use(Router)

export const constantRouterMap = [
  // {
  //   path: '/',
  //   name: 'HelloWorld',
  //   component: HelloWorld
  // },
  {
    path: '/',
    component: () => import('@/views/home/index'),
    hidden: true
  },
  {
    path: '/list',
    component: () =>
      import('@/views/list/index'),
    hidden: true
  },
  {
    path: '/detail/:id',
    component: () =>
      import('@/views/detail/index'),
    hidden: true
  },
  {
    path: '/batch',
    component: () =>
      import('@/views/batch/index'),
    hidden: true
  },
  {
    path: '/404',
    component: () =>
      import('@/views/errorPage/404'),
    hidden: true
  },
  {
    path: '/notFound',
    component: () =>
      import('@/views/errorPage/notFound'),
    hidden: true
  },
  {
    path: '*',
    redirect: '/404',
    hidden: true
  }
]

export default new Router({
  /* 去掉路由地址的#*/
  mode: 'history',
  base: '',
  // 自定义路由切换时页面如何滚动
  scrollBehavior: () => ({
    // return 期望滚动到哪个的位置
    y: 0
  }),
  routes: constantRouterMap
})
