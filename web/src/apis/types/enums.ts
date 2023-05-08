export enum VolType{
    Inside = VolType.INSIDE,
    Outside = VolType.OUTSIDE,
    Large = VolType.LARGE
}
export function getVolTypeName(id: VolType): string {
    switch (id) {
        case VolType.Inside:
            return "校内义工";
        case VolType.Outside:
            return "校外义工";
        case VolType.Large:
            return "大型实践";
        default:
             throw new Error("Invalid enum value");
    }
}

export enum VolStatus{
    Unaudited = VolStatus.UNAUDITED,
    Audited = VolStatus.AUDITED,
    Rejected = VolStatus.REJECTED,
    Finished = VolStatus.FINISHED,
    Deprecated = VolStatus.DEPRECATED
}
export function getVolStatusName(id: VolStatus): string {
    switch (id) {
        case VolStatus.Unaudited:
            return "审核后可报名";
        case VolStatus.Audited:
            return "可报名";
        case VolStatus.Rejected:
            return "不可报名";
        case VolStatus.Finished:
            return "已结束";
        case VolStatus.Deprecated:
            return "过期未审核";
        default:
             throw new Error("Invalid enum value");
    }
}

export enum ThoughtStatus{
    WaitingForSignupAudit = ThoughtStatus.WAITING_FOR_SIGNUP_AUDIT,
    Draft = ThoughtStatus.DRAFT,
    WaitingForFirstAudit = ThoughtStatus.WAITING_FOR_FIRST_AUDIT,
    WaitingForFinalAudit = ThoughtStatus.WAITING_FOR_FINAL_AUDIT,
    Accepted = ThoughtStatus.ACCEPTED
}
export function getThoughtStatusName(id: ThoughtStatus): string {
    switch (id) {
        case ThoughtStatus.WaitingForSignupAudit:
            return "等待报名审核";
        case ThoughtStatus.Draft:
            return "草稿";
        case ThoughtStatus.WaitingForFirstAudit:
            return "等待团支书审核";
        case ThoughtStatus.WaitingForFinalAudit:
            return "等待审计部审核";
        case ThoughtStatus.Accepted:
            return "已通过";
        default:
             throw new Error("Invalid enum value");
    }
}

export enum NoticeType{
    UserNotice = NoticeType.USER_NOTICE,
    ClassNotice = NoticeType.CLASS_NOTICE,
    SchoolNotice = NoticeType.SCHOOL_NOTICE
}
export function getNoticeTypeName(id: NoticeType): string {
    switch (id) {
        case NoticeType.UserNotice:
            return "用户通知";
        case NoticeType.ClassNotice:
            return "班级通知";
        case NoticeType.SchoolNotice:
            return "学校通知";
        default:
             throw new Error("Invalid enum value");
    }
}

export enum Categ{
    None = Categ.NONE,
    Student = Categ.STUDENT,
    Teacher = Categ.TEACHER,
    Class = Categ.CLASS,
    Manager = Categ.MANAGER,
    Auditor = Categ.AUDITOR,
    System = Categ.SYSTEM,
    Inspector = Categ.INSPECTOR,
    Any = Categ.ANY
}
export function getCategName(id: Categ): string {
    switch (id) {
        case Categ.None:
            return "未登录";
        case Categ.Student:
            return "学生";
        case Categ.Teacher:
            return "教师";
        case Categ.Class:
            return "团支书";
        case Categ.Manager:
            return "管理员";
        case Categ.Auditor:
            return "审计部";
        case Categ.System:
            return "系统";
        case Categ.Inspector:
            return "监督员";
        case Categ.Any:
            return "任意";
        default:
             throw new Error("Invalid enum value");
    }
}
