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
        auths: [a.createVol],
        req: structs.VolunteerRecord
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
            auths: [a.updateVol],
            req: structs.VolunteerRecord
        },
        {
            type: "DELETE",
            name: "delete_volunteer",
            auths: [a.deleteVol]
        }
    )
);