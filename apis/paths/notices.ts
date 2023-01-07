import { $ } from "zvms-apis-paths-gen";
import { authData as a } from "../users/index.js";
import { str ,structs} from "../types/index.js";

export default $(
    "/notices",
    [],
    {
        type: "GET",
        name: "search_notices"
    },
    {
        type: "POST",
        name: "send_notice",
        auths: [],
        req: structs.Notice
    },
    $(
        "/<int:id>",
        [],
        {
            type: "GET",
            name: "get_notice",
            desc: ""
        },
        {
            type: "DELETE",
            name: "delete_notice",
            auths: []
        },
        {
            type: "PUT",
            name: "update_notice",
            auths: []
        }
    )
);