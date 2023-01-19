import { int, str, createStructs, arr, createDangerousStructRef, strMaxLength, literal } from "zvms-apis-types-gen";
import { enums } from "./enums.js";

const NoticeBody = {
    title: strMaxLength(32),
    content: strMaxLength(1024),
    deadtime: strMaxLength(19)
}

export const structs = createStructs({
    Class: {
        name: strMaxLength(5)
    },
    NoticeBody,
    Notice: {
        ...NoticeBody,
        type: enums.NoticeType,
        targets: arr(int())
    },
    Report: {
        content: str()
    },
    Signup: {
        stuList: arr(int())
    },
    Thought: {
        content: strMaxLength(1024),
        pictures: arr(str())
    },
    Login: {
        id: int(),
        pwd: strMaxLength(32)
    },
    ModPwd: {
        old: strMaxLength(32),
        new: strMaxLength(32)
    },
    ChangeClass: {
        cls: int()
    },
    UserOfUsers: {
        id: int(),
        name: str(),
        cls: int(),
        auth: int(),
        pwd: str()
    },
    User: {
        name: strMaxLength(5),
        cls: int(),
        auth: int()
    },
    Users: {
        users: arr(createDangerousStructRef("UserOfUsers"))
    },
    VolunteerRecordClass: {
        id: int(),
        max: int()
    },
    Volunteer: {
        name: strMaxLength(32),
        description: strMaxLength(1024),
        time: strMaxLength(20),
        type: literal(enums.VolType.literal.INSIDE,
            enums.VolType.literal.OUTSIDE,
            enums.VolType.literal.LARGE),
        reward: int(),
        classes: arr(createDangerousStructRef("VolunteerRecordClass")),
    },
    Repulse: {
        reason: strMaxLength(1024)
    }
});
