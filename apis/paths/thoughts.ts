import { $ } from "zvms-apis-paths-gen";
import { authData as a } from "../users/index.js";
import { str ,structs} from "../types/index.js";

export default $(
    "/thoughts",
    [],
    {
        type: "GET",
        name: "search_thoughts"
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
                type:"GET",
                name:"get_thought_info",
                auths:[]
            },
            {
                type:"PATCH",
                name:"update_thought",
                auths:[]
            }
        )
    )
);