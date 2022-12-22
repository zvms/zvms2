import { createRouter, createWebHashHistory } from 'vue-router';
import NProgress  from '../plugins/nprogress';

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
		{
			path: '/',
			name: 'home',
			component: () => import('../views/home.vue')
		},
		{
			path: '/login',
			name: 'login',
			component: () => import('../views/login.vue')
		},
		{
			path: '/me',
			name: 'me',
			component: () => import('../views/me.vue')
		},
		{
			path: '/modifyPwd',
			name: 'modifyPwd',
			component: () => import('../views/modifyPwd.vue')
		},
		{
			path: '/logout',
			name: 'logout',
			component: () => import('../views/logout.vue')
		},
		{
			path: '/report',
			name: 'report',
			component: () => import('../views/report.vue')
		},
		{
			path: '/class/list',
			name: 'classList',
			component: () => import('../views/class/list.vue')
		},
		{
			path: '/class/stulist/:classid',
			name: 'classStulist',
			component: () => import('../views/class/stulist.vue')
		},
		{
			path: '/volunteer/list',
			name: 'volunteerList',
			component: () => import('../views/volunteer/list.vue')
		},
		{
			path: '/volunteer/create',
			name: 'volunteerCreate',
			component: () => import('../views/volunteer/create.vue')
		},
		{
			path: '/volunteer/audit',
			name: 'volunteerAudit',
			component: () => import('../views/volunteer/audit.vue')
		},
		{
			path: '/volunteer/holiday',
			name: 'volunteerHoliday',
			component: () => import('../views/volunteer/holiday.vue')
		},
		{
			path: '/volunteer/thought',
			name: 'volunteerThought',
			component: () => import('../views/volunteer/thought.vue')
		},
		{
			path: '/notice',
			name: 'noticeCreate',
			component: () => import('../views/notice.vue')
		},
		{
			path: '/about',
			name: 'about',
			component: () => import('../views/about.vue')
		}
	]
})


router.afterEach(() => {
  NProgress.done()
})

export default router
