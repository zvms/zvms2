import { Part } from "../types.js";
import { tsPath } from "./path.js";

const tsAddBeforeFile = `
import {get, post} from "./utils";
import * as structs from "../types/structs";
`;
const tsAddAfterFile = "";

export function genTs(name: string, part: Part): string {
    let str = tsAddBeforeFile;
    str += tsPath(name, part);
    str += tsAddAfterFile;
    str = str;
    return str;
}