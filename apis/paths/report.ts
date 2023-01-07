import { $ } from "zvms-apis-paths-gen";
import { str, structs } from "../types/index.js";

export default $(
    "/report",
    [],
    {
        type: "POST",
        name: "report",
        req: {
            content: str()
        }
    }
);