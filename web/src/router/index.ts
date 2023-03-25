import { Categ } from "@/apis";
import { useInfoStore } from "@/stores";
import { createRouter, createWebHashHistory } from "vue-router";

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      name: "login",
      component: () => import("../views/login.vue"),
    },
    {
      path: "/",
      name: "me",
      component: () => import("../views/me.vue"),
    },
    {
      path: "/modifyPwd",
      name: "modifyPwd",
      component: () => import("../views/modify-pwd.vue"),
    },
    // {
    //   path: "/class/list",
    //   name: "classList",
    //   component: () => import("../views/class/list.vue"),
    // },
    // {
    //   path: "/class/stulist/:classid",
    //   name: "classStulist",
    //   component: () => import("../views/class/stu-list.vue"),
    // },
    {
      path: "/volunteer/list",
      name: "volunteerList",
      component: () => import("../views/volunteer/list.vue"),
    },
    {
      path: "/volunteer/create",
      name: "volunteerCreate",
      component: () => import("../views/volunteer/create.vue"),
    },
    // {
    //   path: "/volunteer/firstAudit",
    //   name: "volunteerFirstAudit",
    //   component: () => import("../views/volunteer/first-audit.vue"),
    // },
    {
      path: "/volunteer/finalAudit",
      name: "volunteerFinalAudit",
      component: () => import("../views/volunteer/final-audit.vue"),
    },
    // {
    //   path: "/volunteer/holiday",
    //   name: "volunteerHoliday",
    //   component: () => import("../views/volunteer/holiday.vue"),
    // },
    // {
    //   path: "/volunteer/thought",
    //   name: "volunteerThought",
    //   component: () => import("../views/volunteer/thought.vue"),
    // },
    // {
    //   path: "/sendNotice",
    //   name: "sendNotice",
    //   component: () => import("../views/send_notice.vue"),
    // },
    {
      path: "/about",
      name: "about",
      component: () => import("../views/about.vue"),
    },
  ],
});

router.beforeEach((to, from, next) => {
  /* 页面title */
  if (to.name !== "login" && to.name !== "about") {
    const infoStore = useInfoStore();
    if (!infoStore.token || infoStore.permission & Categ.None) {
      next({
        path: "/login",
      });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
