import { Config, Params } from "./types.js";

export function path2LCamal(path: string) {
    let s = "";
    let isFirstLetter = true;
    let isParamName = false;
    let isParamType = false;
    let params: { name: string, type: string }[] = [];
    for (const c of path) {
        if (c === "/") {
            isFirstLetter = true;
        } else if (c === "<") {
            isFirstLetter = false;
            isParamName = true;
            params.push({ name: "", type: "" })
        } else if (c === ">") {
            isFirstLetter = false;
            isParamName = false;
            isParamType = false;
        } else if (c === ">") {
            isFirstLetter = false;
            isParamName = false;
            isParamType = false;
        } else {
            if (isParamName) {
                params[params.length - 1].name += c;
            } else if (isParamType) {
                params[params.length - 1].type += c;
            } else {
                s += isFirstLetter ? c.toUpperCase() : c;
            }
            isFirstLetter = false;
        }
    }
    if (params.length > 0) {
        s += "By" + params.map(({ name }) => {
            return name[0].toUpperCase() + name.slice(1)
        }).join("");
    }
    return s;
}


export function cfg2str(cfg?: Config) {
    if (!cfg) return "";
}

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