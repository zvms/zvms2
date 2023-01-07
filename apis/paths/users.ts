import { $ } from "zvms-apis-paths-gen";
import { authData as a } from "../users/index.js";
import { str ,structs} from "../types/index.js";

export default $(
    "/users",
    [],
    {
        type: "GET",
        name: "search_users",
        auths:[a.readMyUserInfo]
    },
    {
        type: "POST",
        name: "create_users",
        auths: [a.writeUserInfo],
        req: structs.Users
    },
    $(
        "/check",
        [],
        {
            type:"GET",
            name:"check"
        }
    ),
    $(
        "/login",
        [],
        {
            type:"POST",
            name:"login",
            auths:[a.login],
            req:structs.Login
        }
    ),
    $(
        "/logout",
        [],
        {
            type:"POST",
            name:"logout"
        }
    ),
    $(
        "/mod-pwd",
        [],
        {
            type:"PATCH",
            name:"modify_password",
            req:structs.ModPwd
        }
    ),
    $(
        "/change-class",
        [],
        {
            type:"PATCH",
            name:"change_class",
            req:structs.ChangeClass
        }
    ),
    $(
        "/<int:id>",
        [a.readMyUserInfo],
        {
            type: "GET",
            name: "get_user_info"
        },
        {
            type: "DELETE",
            name: "delete_user",
            auths: [a.writeUserInfo]
        },
        {
            type: "PUT",
            name: "modify_user",
            auths: [a.writeUserInfo]
        }
    )
);