import { int, str, createStructs, arr, createDangerousStructRef, strMaxLength } from "zvms-apis-types-gen";
import { enums } from "./enums";

const NoticeBody = {
    title: str(),
    content: str(),
    deadtime: str()
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
        pictures: arr(strMaxLength(32))
    },
    Login: {
        id:int(),
        pwd:strMaxLength(32)
    },
    ModPwd:{
        old:strMaxLength(32),
        new:strMaxLength(32)
    },
    ChangeClass:{
        cls:int()
    },
    VolunteerRecordClass: {
        id: int(),
        max: int()
    },
    UserOfUsers: {
        id: int(),
        name: str(),
        cls: int(),
        auth: int(),
        pwd: str()
    },
    Users: {
        users: arr(createDangerousStructRef("UserOfUsers"))
    },
    User: {
        name: str(),
        cls: int(),
        auth: int()
    },
    VolunteerRecord: {
        name: str(),
        description: str(),
        time: str(),
        type: int(),
        reward: int(),
        classes: arr(createDangerousStructRef("VolunteerRecordClass")),
    }
});