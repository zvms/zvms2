export class VolType {
    Inside = new VolType(1);
    Outside = new VolType(2);
    Large = new VolType(3);
    private constructor(public id: Number) { }
    get name(): string {
        switch (this.id) {
            case 1:
                return "校内义工";
            case 2:
                return "校外义工";
            case 3:
                return "大型实践";
            default:
                throw new Error("Invalid enum id");
        }
    }
}
export class NoticeType {
    User = new NoticeType(1);
    Cls = new NoticeType(2);
    School = new NoticeType(3);
    private constructor(public id: Number) { }
    get name(): string {
        switch (this.id) {
            case 1:
                return "用户通知";
            case 2:
                return "班级通知";
            case 3:
                return "学校通知";
            default:
                throw new Error("Invalid enum id");
        }
    }
}
export class VolStatus {
    Unaudited = new VolStatus(1);
    Audited = new VolStatus(2);
    private constructor(public id: Number) { }
    get name(): string {
        switch (this.id) {
            case 1:
                return "未过审";
            case 2:
                return "已过审";
            default:
                throw new Error("Invalid enum id");
        }
    }
}
export class ThoughtStatus {
    WaitingForSignupAudit = new ThoughtStatus(1);
    Unsubmitted = new ThoughtStatus(2);
    Draft = new ThoughtStatus(3);
    WaitingForFirstAudit = new ThoughtStatus(4);
    WaitingForFinalAudit = new ThoughtStatus(5);
    Accepted = new ThoughtStatus(6);
    private constructor(public id: Number) { }
    get name(): string {
        switch (this.id) {
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
                throw new Error("Invalid enum id");
        }
    }
}
export class Categ {
    None = new Categ(1);
    Student = new Categ(2);
    Teacher = new Categ(4);
    Class = new Categ(8);
    Manager = new Categ(16);
    Auditor = new Categ(32);
    System = new Categ(64);
    private constructor(public id: Number) { }
    get name(): string {
        switch (this.id) {
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
                throw new Error("Invalid enum id");
        }
    }
}
