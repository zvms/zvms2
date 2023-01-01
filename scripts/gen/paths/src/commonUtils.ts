import { Params } from "./types.js";

export function req2paramsApply(req?: Params): string {
    if (!req) return "";
    let ks: string[] = [];
    for (const k in req) {
        ks.push(paramName(k));
    }
    return ks.join(",\n");
}

export function paramName(n: string) {
    return n === "class" ? `classId` : n;
}

export function snack2camal(str: string, upperCaseFirst = false) {
    let result = "", upperCase = upperCaseFirst;
    for (let c of str) {
        if (c === "_") upperCase = true;
        else if (upperCase) {
            upperCase = false;
            c = c.toUpperCase();
        }
        result += c;
    }
    return result;
}