import { Params } from "./types.js";

export function req2paramsApply(req?: Params): string {
    if (!req) return "";
    const ks: string[] = [];
    for (const k in req) {
        ks.push(paramName(k));
    }
    return ks.join(",\n");
}

export function paramName(n: string) {
    return n === "class" ? `classId` : n;
}