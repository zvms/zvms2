import { Apis } from "../types.js";
import { tsPath } from "./path.js";

export function genTs(apis: Apis, fApiTemplate: string): string {
    let str = "";
    for (const part of apis) {
        str += tsPath({
            fileName: part.name.slice(1),
            path: ""
        }, part);
    }
    return fApiTemplate.replace("//${METHODS}", str);
}