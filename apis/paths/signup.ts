import { $ } from "zvms-apis-paths-gen";
import { authData as a } from "../users/index.js";
import { int } from "../types/index.js";

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
            type: "POST",
            name: "signup",
            desc: "",
            req: {
                volId: int()
            }
        },
        $(
            "/<int:volId>",
            [],
            {
                type: "PATCH",
                name: "audit_signup",
                auths: [a.auditSignup]
            },
            {
                type: "DELETE",
                name: "rollback",
                auths: [a.rollbackSignup]
            }
        )
    )
);