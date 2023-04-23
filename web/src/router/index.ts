import { Categ } from "@/apis";
import { useInfoStore } from "@/stores";
import { createRouter, createWebHistory } from "vue-router";

export interface NavItemInfo {
  title: string;
  icon: string;
}

type AuthedFunc = (permission: Categ) => boolean;

declare module "vue-router" {
  interface RouteMeta {
    authed: AuthedFunc;
    nav?: NavItemInfo;
  }
}

function createHasAuth(auth: Categ): AuthedFunc {
  return (permission: Categ) => (auth & permission) > 0;
}

function createHasnotAuth(auth: Categ): AuthedFunc {
  return (permission: Categ) => (auth & permission) === 0;
}

const unloginedAuth = createHasAuth(Categ.None);
const loginedAuth = createHasnotAuth(Categ.None);
const anyAuth: AuthedFunc = () => true;

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "me",
      component: () => import("../views/me.vue"),
      meta: {
        authed: loginedAuth,
        nav: {
          title: "我的",
          icon: "mdi-account-circle",
        },
      },
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/login.vue"),
      meta: {
        authed: unloginedAuth,
        nav: {
          title: "登录",
          icon: "mdi-account-circle",
        },
      },
    },
    {
      path: "/volunteer/list",
      name: "volunteerList",
      component: () => import("../views/volunteer/list.vue"),
      meta: {
        authed: loginedAuth,
        nav: {
          title: "义工列表",
          icon: "mdi-format-list-text",
        },
      },
    },
    {
      path: "/volunteer/create",
      name: "volunteerCreate",
      component: () => import("../views/volunteer/create.vue"),
      meta: {
        authed: loginedAuth,
        nav: {
          title: "创建义工",
          icon: "mdi-folder-multiple-plus",
        },
      },
    },
    {
      path: "/volunteer/record",
      name: "volunteerRecord",
      component: () => import("../views/volunteer/record.vue"),
      meta: {
        authed: createHasAuth(Categ.Manager | Categ.System | Categ.Auditor),
        nav: {
          title: "记录义工",
          icon: "mdi-folder-multiple-plus",
        },
      },
    },
    {
      path: "/volunteer/finalAudit",
      name: "volunteerFinalAudit",
      component: () => import("../views/volunteer/final-audit.vue"),
      meta: {
        authed: createHasAuth(Categ.System | Categ.Auditor),
        nav: {
          title: "审核感想",
          icon: "mdi-check-circle",
        },
      },
    },
    {
      path: "/notice/create",
      name: "noticeCreate",
      component: () => import("../views/notice/create.vue"),
      meta: {
        authed: createHasAuth(Categ.System | Categ.Manager),
        nav: {
          title: "创建通知",
          icon: "mdi-message-draw",
        },
      },
    },
    {
      path: "/about",
      name: "about",
      component: () => import("../views/about.vue"),
      meta: {
        authed: anyAuth,
        nav: {
          title: "关于我们",
          icon: "mdi-information",
        },
      },
    },
    {
      path: "/system/ttyd",
      name: "systemTtyd",
      component: () => import("../views/system/ttyd.vue"),
      meta: {
        authed: createHasAuth(Categ.System),
        nav: {
          title: "TTYD",
          icon: "mdi-powershell",
        },
      },
    },
    {
      path: "/system/view-report",
      name: "systemViewReport",
      component: () => import("../views/system/view-report.vue"),
      meta: {
        authed: createHasAuth(Categ.System),
        nav: {
          title: "查看反馈",
          icon: "mdi-comment-quote",
        },
      },
    },
  ],
});

router.beforeEach((to, _from, next) => {
  const infoStore = useInfoStore();
  if (!to.meta.authed(infoStore.permission)) {
    next("/login");
  } else {
    next();
  }
});

export default router;
