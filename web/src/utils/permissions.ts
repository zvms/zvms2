export enum permissionTypes {
    none = 0,
    logined = 1,
    secretary = 2,
    teacher = 3,
    admin = 4,
    _super = 5,
    system = 6
}

export const permissionNames = {
    [permissionTypes.none]:"未登录！",
    [permissionTypes.logined]:"用户",
    [permissionTypes.secretary]: "团支书",
    [permissionTypes.teacher]: "教师",
    [permissionTypes.admin]: "管理员",
    [permissionTypes.system]: "系统",
    [permissionTypes._super]: "超管",
}