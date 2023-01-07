import { int, str, createStructs, arr, createDangerousStructRef } from "zvms-apis-types-gen";

const NoticeBody = {
    title: str(),
    content: str(),
    deadtime: str()
}

export const structs = createStructs({
    NoticeBody,
    Notice: {
        ...NoticeBody,
        type: int(),
        targets: arr(int())
    },
    Report: {
        content: str()
    },
    Signup: {
        volId: int(),
    },
    Login: {
        id: int(),
        pwd: str()
    },
    ModPwd: {
        old: str(),
        new: str()
    },
    ChangeClass: {
        clsId: int()
    },
    VolunteerRecordClass: {
        id: int(),
        max: int()
    },
    VolunteerRecord: {
        name: str(),
        description: str(),
        time: str(),
        type: int(),
        reward: int(),
        classes: arr(createDangerousStructRef("VolunteerRecordClass")),
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
    }
});