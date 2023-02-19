export enum VolType {
    INSIDE = 1,
    OUTSIDE = 2,
    LARGE = 3
}
export function getVolTypeName(id: VolType): string {
    switch (id) {
        case VolType.INSIDE:
            return "校内义工";
        case VolType.OUTSIDE:
            return "校外义工";
        case VolType.LARGE:
            return "大型实践";

    default:
        throw Error("Invalid enum value");
    }
}
export enum VolStatus {
    UNAUDITED = 1,
    AUDITED = 2
}
export function getVolStatusName(id: VolStatus): string {
    switch (id) {
        case VolStatus.UNAUDITED:
            return "未过审";
        case VolStatus.AUDITED:
            return "已过审";

    default:
        throw Error("Invalid enum value");
    }
}
export enum ThoughtStatus {
    WAITING_FOR_SIGNUP_AUDIT = 1,
    UNSUBMITTED = 2,
    DRAFT = 3,
    WAITING_FOR_FIRST_AUDIT = 4,
    WAITING_FOR_FINAL_AUDIT = 5,
    ACCEPTED = 6
}
export function getThoughtStatusName(id: ThoughtStatus): string {
    switch (id) {
        case ThoughtStatus.WAITING_FOR_SIGNUP_AUDIT:
            return "等待报名审核";
        case ThoughtStatus.UNSUBMITTED:
            return "未填写";
        case ThoughtStatus.DRAFT:
            return "草稿";
        case ThoughtStatus.WAITING_FOR_FIRST_AUDIT:
            return "等待初审";
        case ThoughtStatus.WAITING_FOR_FINAL_AUDIT:
            return "等待终审";
        case ThoughtStatus.ACCEPTED:
            return "已通过";

    default:
        throw Error("Invalid enum value");
    }
}
export enum NoticeType {
    USER_NOTICE = 1,
    CLASS_NOTICE = 2,
    SCHOOL_NOTICE = 3
}
export function getNoticeTypeName(id: NoticeType): string {
    switch (id) {
        case NoticeType.USER_NOTICE:
            return "用户通知";
        case NoticeType.CLASS_NOTICE:
            return "班级通知";
        case NoticeType.SCHOOL_NOTICE:
            return "学校通知";

    default:
        throw Error("Invalid enum value");
    }
}
export enum Categ {
    NONE = 1,
    STUDENT = 2,
    TEACHER = 4,
    CLASS = 8,
    MANAGER = 16,
    AUDITOR = 32,
    SYSTEM = 64,
    ANY = 127
}
export function getCategName(id: Categ): string {
    switch (id) {
        case Categ.NONE:
            return "未登录";
        case Categ.STUDENT:
            return "学生";
        case Categ.TEACHER:
            return "教师";
        case Categ.CLASS:
            return "班级";
        case Categ.MANAGER:
            return "管理员";
        case Categ.AUDITOR:
            return "审计部";
        case Categ.SYSTEM:
            return "系统";
        case Categ.ANY:
            return "任意";

    default:
        throw Error("Invalid enum value");
    }
}
