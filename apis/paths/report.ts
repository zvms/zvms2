import { $ } from "zvms-apis-paths-gen";
import { structs } from "../types/index.js";

export default $(
    "/report",
    [],
    {
        type: "POST",
        name: "report",
        req: structs.Report
    }
);