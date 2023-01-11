import { PathItem } from "../types.js";
import { tsPath } from "./path.js";

const tsAddBeforeFile = `import {get, post} from "./utils.js";
import * as structs from "../types/structs.js";
import * as enums from "../types/enums.js";
`;
const tsAddAfterFile = "";

export function genTs(part: PathItem): string {
    let str = tsAddBeforeFile;
    str += tsPath({
        fileName: part.name.slice(1),
        path: ""
    }, part);
    str += tsAddAfterFile;
    return str;
}