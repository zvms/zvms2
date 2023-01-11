import { $ } from "zvms-apis-paths-gen";
import { authData as a } from "../users/index.js";
import { str } from "../types/index.js";

export default $(
    "/classes",
    {
        type: "GET",
        name: "list_classes",
        auths: [a.readAnyClass]
    },
    {
        type: "POST",
        name: "create_class",
        auths: [a.writeClass],
        req: {
            name: str()
        }
    },
    $(
        "/<int:id>",
        {
            type: "GET",
            name: "get_class_info",
            desc: ""
        },
        {
            type: "DELETE",
            name: "delete_class",
            auths: [a.writeClass]
        },
        {
            type: "PUT",
            name: "modify_class",
            auths: [a.writeClass]
        }
    )
);