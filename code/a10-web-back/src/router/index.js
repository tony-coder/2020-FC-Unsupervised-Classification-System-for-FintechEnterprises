import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '控制台', icon: 'dashboard' }
    }]
  },
  {
    path: '/statisic',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'statisic',
        component: () => import('@/views/statisic/index'),
        meta: { title: '统计数据参考', icon: 'statisic' }
      }
    ]
  },
  // {
  //   path: '/tag',
  //   component: Layout,
  //   children: [
  //     {
  //       path: 'index',
  //       name: 'tag',
  //       component: () => import('@/views/tag/index'),
  //       meta: { title: '企业标签分析', icon: 'tag' }
  //     }
  //   ]
  // },
  {
    path: '/cluster',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'cluster',
        component: () => import('@/views/cluster/index'),
        meta: { title: '企业聚类分析', icon: 'box' }
      }
    ]
  },
  {
    path: '/upload',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'upload',
        component: () => import('@/views/upload/index'),
        meta: { title: '数据上传', icon: 'upload' }
      }
    ]
  },
  {
    path: '/test',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'upload',
        component: () => import('@/views/test/index'),
        meta: { title: '数据测试', icon: 'test' }
      }
    ]
  },
  {
    path: '/model',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'model',
        component: () => import('@/views/model/index'),
        meta: { title: '模型数据调整', icon: 'setting' }
      }
    ]
  },
  {
    path: '/info',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'info',
        component: () => import('@/views/about/index'),
        meta: { title: '关于e企查', icon: 'info' }
      }
    ]
  },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
