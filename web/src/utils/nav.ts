import { useNavStore, useInfoStore } from "@/stores";
import { permissionTypes } from "./permissions";

interface NavItem {
  title: string;
  to: string;
  icon: string;
}

export function getNavItems(permission: permissionTypes) {
  const navItems = {
    login: {
      title: "登录",
      to: "/login",
      icon: "mdi-account-circle",
    },
    me: {
      title: "我的",
      to: "/",
      icon: "mdi-account-circle",
    },
    // modifyPwd: {
    //   title: "修改密码",
    //   to: "/modifyPwd",
    //   icon: "mdi-lock",
    // },
    // classList: {
    //   title: "班级列表",
    //   to: "/class/list",
    //   icon: "mdi-view-list",
    // },
    // stuList: {
    //   title: "学生列表",
    //   to: "/class/stulist/0",
    //   icon: "mdi-format-list-bulleted-square",
    // },
    volList: {
      title: "义工列表",
      to: "/volunteer/list",
      icon: "mdi-format-list-text",
    },
    // notice: {
    //   title: "创建通知",
    //   to: "/sendNotice",
    //   icon: "mdi-message-draw",
    // },
    createVol: {
      title: "创建义工",
      to: "/volunteer/create",
      icon: "mdi-folder-multiple-plus",
    },
    // firstAuditVol: {
    //   title: "初审感想",
    //   to: "/volunteer/firstAudit",
    //   icon: "mdi-check-circle",
    // },
    finalAuditVol: {
      title: "终审感想",
      to: "/volunteer/finalAudit",
      icon: "mdi-check-circle",
    },
    // holidayVol: {
    //   title: "义工自提交",
    //   to: "/volunteer/holiday",
    //   icon: "mdi-cloud-upload",
    // },
    // uploadThought: {
    //   title: "感想提交",
    //   to: "/volunteer/thought",
    //   icon: "mdi-upload",
    // },
    report: {
      title: "反馈错误",
      to: "/report",
      icon: "mdi-alert",
    },
    about: {
      title: "关于我们",
      to: "/about",
      icon: "mdi-help-circle",
    },
  } satisfies Record<string, NavItem>;

  const items: NavItem[] = [];

  if (!(permission & permissionTypes.logined)) items.push(navItems.login);
  if (permission & permissionTypes.logined) items.push(navItems.volList);
  if (permission & permissionTypes.logined) items.push(navItems.createVol);
  if (permission & permissionTypes.system) items.push(navItems.finalAuditVol);
  items.push(navItems.report);
  items.push(navItems.about);
  return items;
}

export function applyNavItems() {
  return (useNavStore().items = getNavItems(
    useInfoStore().permission || permissionTypes.none
  ));
}
