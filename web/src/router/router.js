import Vue from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

router.beforeEach((to, from, next) => {
	NProgress.start();
	if (to.path == '/report' || to.path == '/about') next();
	else if (to.path != '/login') {
		// console.log(233);
		// console.log(to,from,next);
        // console.log(store.state.token);
		// console.log(233);
		if (store.state.token) {
			next();
		} else {
			next('login');
		}
	} else if(store.state.token){
		next('me');
		// next()
	} else {
		next();
	}
})