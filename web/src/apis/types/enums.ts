export enum Categ {
    None = 1,
    Student = 2,
    Teacher = 4,
    Class = 8,
    Manager = 16,
    Auditor = 32,
    System = 64
}
export function getCategName(id: number) {
    switch (id) {
        case 1:
            return "未登录";
        case 2:
            return "学生";
        case 4:
            return "教师";
        case 8:
            return "班级";
        case 16:
            return "管理";
        case 32:
            return "审计部";
        case 64:
            return "系统";
        default:
            throw Error("Invalid enum value");
    }
}
export enum NoticeType {
    User = 1,
    Cls = 2,
    School = 3
}
export function getNoticeTypeName(id: number) {
    switch (id) {
        case 1:
            return "用户通知";
        case 2:
            return "班级通知";
        case 3:
            return "学校通知";
        default:
            throw Error("Invalid enum value");
    }
}
export enum ThoughtStatus {
    WaitingForSignupAudit = 1,
    Unsubmitted = 2,
    Draft = 3,
    WaitingForFirstAudit = 4,
    WaitingForFinalAudit = 5,
    Accepted = 6
}
export function getThoughtStatusName(id: number) {
    switch (id) {
        case 1:
            return "等待报名审核";
        case 2:
            return "未填写";
        case 3:
            return "草稿";
        case 4:
            return "等待初审";
        case 5:
            return "等待终审";
        case 6:
            return "已通过";
        default:
            throw Error("Invalid enum value");
    }
}
export enum VolStatus {
    Unaudited = 1,
    Audited = 2
}
export function getVolStatusName(id: number) {
    switch (id) {
        case 1:
            return "未过审";
        case 2:
            return "已过审";
        default:
            throw Error("Invalid enum value");
    }
}
export enum VolType {
    Inside = 1,
    Outside = 2,
    Large = 3
}
export function getVolTypeName(id: number) {
    switch (id) {
        case 1:
            return "校内义工";
        case 2:
            return "校外义工";
        case 3:
            return "大型实践";
        default:
            throw Error("Invalid enum value");
    }
}
