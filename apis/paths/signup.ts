import { $ } from "zvms-apis-paths-gen";
import { authData as a } from "../users/index.js";
import { str ,structs} from "../types/index.js";

export default $(
    "/signup",
    [],
    {
        type: "GET",
        name: "list_signup"
    },
    $(
        "/<int:stuId>",
        [],
        {
            type: "GET",
            name: "signup",
            desc: "",
            req:structs.Signup
        },
        $(
            "/<int:volId>",
            [],
            {
                type:"PATCH",
                name:"audit_signup",
                auths:[a.auditSignup]
            },
            {
                type:"DELETE",
                name:"rollback",
                auths:[a.rollbackSignup]
            }
        )
    )
);