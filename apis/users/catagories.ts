import {createUserCatagories} from "zvms-apis-users-gen"

export const userCatagories = createUserCatagories({
    none:{
        id:0b00000001,
        name:"未登录"
    },
    student:{
        id:0b00000010,
        name:"学生"
    },
    teacher:{
        id:0b00000100,
        name:"教师"
    },
    aclass:{
        id:0b00001000,
        name:"班级"
    },
    manager:{
        id:0b00010000,
        name:"管理"
    },
    auditor:{
        id:0b00100000,
        name:"审计部"
    },
    system:{
        id:0b01000000,
        name:"系统"
    }
})