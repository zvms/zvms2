import { useNavStore, useInfoStore } from "@/stores";
import { Categ } from "@/apis/types/enums";

export interface NavItem {
  title: string;
  to: string;
  icon: string;
}

export function getNavItems(permission: Categ) {
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
    createNotice: {
      title: "创建通知",
      to: "/notice/create",
      icon: "mdi-message-draw",
    },
    createVol: {
      title: "创建义工",
      to: "/volunteer/create",
      icon: "mdi-folder-multiple-plus",
    },
    recordVol: {
      title: "记录义工",
      to: "/volunteer/record",
      icon: "mdi-folder-multiple-plus",
    },
    // firstAuditVol: {
    //   title: "初审感想",
    //   to: "/volunteer/firstAudit",
    //   icon: "mdi-check-circle",
    // },
    finalAuditVol: {
      title: "审核感想",
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
    about: {
      title: "关于我们",
      to: "/about",
      icon: "mdi-information",
    },
    ttyd: {
      title: "TTYD",
      to: "/system/ttyd",
      icon: "mdi-powershell",
    },
    viewReport: {
      title: "查看反馈",
      to: "/system/view-report",
      icon: "mdi-comment-quote",
    }
  } as const satisfies Record<string, NavItem>;

  const items: NavItem[] = [];

  if (permission & Categ.None) items.push(navItems.login);
  if (!(permission & Categ.None)) items.push(navItems.me);
  if (!(permission & Categ.None)) items.push(navItems.volList);
  if (!(permission & Categ.None)) items.push(navItems.createVol);
  if (permission & (Categ.System | Categ.Auditor | Categ.Manager))
    items.push(navItems.recordVol);
  if (permission & (Categ.System | Categ.Auditor | Categ.Manager))
    items.push(navItems.finalAuditVol);
  if (permission & (Categ.System | Categ.Manager))
    items.push(navItems.createNotice);
  if (permission & Categ.System) items.push(navItems.ttyd);
  if (permission & Categ.System) items.push(navItems.viewReport);
  items.push(navItems.about);
  return items;
}

export function applyNavItems() {
  return (useNavStore().items = getNavItems(
    useInfoStore().permission || Categ.None
  ));
}
