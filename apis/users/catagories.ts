import {createUserCatagories} from "zvms-apis-users-gen"

export const userCatagories = createUserCatagories({
    none:{
        id:0x1,
        name:"未登录"
    },
    student:{
        id:0x2,
        name:"学生"
    }
})