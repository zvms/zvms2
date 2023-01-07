import { $ } from "zvms-apis-paths-gen";
import { authData as a } from "../users/index.js";
import { str, structs } from "../types/index.js";

export default $(
    "/volunteers",
    [],
    {
        type: "GET",
        name: "search_volunteers"
    },
    {
        type: "POST",
        name: "create_volunteer",
        auths: [],
        req: structs.VolunteerRecord.raw
    },
    $(
        "/<int:id>",
        [],
        {
            type: "GET",
            name: "get_volunteer_info",
            desc: ""
        },
        {
            type: "PUT",
            name: "update_volunteer",
            auths: [],
            req: structs.VolunteerRecord.raw
        },
        {
            type: "DELETE",
            name: "delete_volunteer",
            auths: []
        }
    )
);