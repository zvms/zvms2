import { PathItem } from "../types.js";
import { tsPath } from "./path.js";

const tsAddBeforeFile = `import {get, post} from "./utils";
import * as structs from "../types/structs";
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