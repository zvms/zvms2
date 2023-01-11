import { Apis } from "./types";

export function fApiIndexRaw(data: Apis) {
    return data.map(v => `export * from "./${v.name}.js";`).join("\n");
}

export function viewsInitRaw(data: Apis) {
    return "__ALL__ = [\n"
        + data.map(v => `    '${v.name}'`).join(",\n")
        + "\n]";
}

export function implsInitRaw(data: Apis) {
    return "__ALL__ = [\n"
        + data.map(v => `    '${v.name}'`).join(",\n")
        + "\n]";
}