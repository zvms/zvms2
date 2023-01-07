import { $ } from "zvms-apis-paths-gen";
import { authData as a } from "../users/index.js";
import { int, str, arr, structs } from "../types/index.js";

export default $(
    "/users",
    [],
    {
        type: "GET",
        name: "search_users",
        auths: [a.readMyUserInfo]
    },
    {
        type: "POST",
        name: "create_users",
        auths: [a.writeUserInfo],
        req: {
            users: arr(structs.UserOfUsers)
        }
    },
    $(
        "/check",
        [],
        {
            type: "GET",
            name: "check"
        }
    ),
    $(
        "/login",
        [],
        {
            type: "POST",
            name: "login",
            auths: [a.login],
            req: {
                id: int(),
                pwd: str()
            },
        }
    ),
    $(
        "/logout",
        [],
        {
            type: "POST",
            name: "logout"
        }
    ),
    $(
        "/mod-pwd",
        [],
        {
            type: "PATCH",
            name: "modify_password",
            req: {
                old: str(),
                new: str()
            }
        }
    ),
    $(
        "/change-class",
        [],
        {
            type: "PATCH",
            name: "change_class",
            req: {
                newClsId: int()
            }
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