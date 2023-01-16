import { Method, Params } from "../types.js";
import { paramName } from "../commonUtils.js";

export * from "../commonUtils.js";

export function tsReq2paramsDecl(req?: Params): string {
    if (!req) return "";
    let ks: string[] = [];
    for (const k in req) {
        ks.push(paramName(k) + ": " + req[k].ts);
    }
    return ks.join(",\n");
}

export function tsReq2paramsDesc(req?: Params): string[] {
    if (!req) return [];
    let descs: string[] = [];
    for (const k in req) {
        descs.push(` * @param ${paramName(k)} ${req[k].desc || ""}`)
    }
    return descs;
}

export function tsResType(res?: Params) {
    if (!res) return "[]";
    let members = "";
    for (const k in res) {
        members += `${tsCommentStr(res[k].desc)}${paramName(k)}: ${res[k].ts},`;
    }
    return "[" + members + "]";
}

export function tsComments(m: Method) {
    return `${tsAddStar(m.desc)}${tsReq2paramsDesc(m.req).join("\n")}`
}

export function tsAddStar(str: string | undefined) {
    return str ? "\n * " + str : "";
}

export function tsCommentStr(comment?: string) {
    return comment ?
        `/** ${comment} */` :
        "";
}