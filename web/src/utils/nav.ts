import { useDrawerStore, useInfoStore } from "@/stores";
import { permissionTypes } from "./permissions"


export function getNavItems(permission:permissionTypes) {
    let navItems = {
        me: {
            title: "我的",
            to: "/me",
            icon: "mdi-account-circle"
        },
        modifyPwd: {
            title: "修改密码",
            to: "/modifyPwd",
            icon: "mdi-lock"
        },
        classList: {
            title: "班级列表",
            to: "/class/list",
            icon: "mdi-view-list",
        },
        stuList: {
            title: "学生列表",
            to: "/class/stulist/0",
            icon: "mdi-format-list-bulleted-square",
        },
        volList: {
            title: "义工列表",
            to: "/volunteer/list",
            icon: "mdi-format-list-text",
        },
        notice: {
            title: "创建通知",
            to: "/notice",
            icon: "mdi-message-draw",
        },
        createVol: {
            title: "创建义工",
            to: "/volunteer/create",
            icon: "mdi-folder-multiple-plus",
        },
        auditVol: {
            title: "审核感想",
            to: "/volunteer/audit",
            icon: "mdi-check-circle",
        },
        holidayVol: {
            title: "义工自提交",
            to: "/volunteer/holiday",
            icon: "mdi-cloud-upload",
        },
        uploadThought: {
            title: "感想提交",
            to: "/volunteer/thought",
            icon: "mdi-upload",
        },
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
        logout: {
            title: "登出",
            to: "/logout",
            icon: "mdi-exit-to-app",
        }
    };

    let items = [];
    if (permission >= permissionTypes.logined) {
        items.push(navItems.me);
        items.push(navItems.modifyPwd);
    }
    if (permission >= permissionTypes.teacher) {
        items.push(navItems.classList);
    }
    if (permission >= permissionTypes.secretary) {
        items.push(navItems.stuList);
    }
    if (permission >= permissionTypes.secretary) {
        items.push(navItems.volList);
    }
    if (permission >= permissionTypes.teacher) {
        items.push(navItems.notice);
    }
    if (permission >= permissionTypes.teacher
        && permission != permissionTypes.admin) {
        items.push(navItems.createVol);
    }
    if (permission > permissionTypes.teacher) {
        items.push(navItems.auditVol);
    }
    if (permission == permissionTypes.secretary) {
        items.push(navItems.holidayVol, navItems.uploadThought);
    }
    items.push(navItems.report);
    items.push(navItems.about);
    if (permission >= permissionTypes.logined) {
        items.push(navItems.logout);
    }
    return items;
}

export function applyNavItems() {
    console.log(this.infoStore.permission);
    return useDrawerStore().items = getNavItems(this.infoStore.permission || permissionTypes.none);
}