import { Type, Description } from "./types.js";

export function arr(type: Type, desc?: Description): Type {
    return {
        ts: `Array<${type.ts}>`,
        py: `typing.Sequence[${type.py}]`,
        desc
    }
}
export function str(desc?: Description): Type {
    return {
        ts: "string",
        py: "str",
        desc
    }
}
export function int(desc?: Description): Type {
    return {
        ts: "number",
        py: "int",
        desc
    }
}
export function float(desc?: Description): Type {
    return {
        ts: "number",
        py: "float",
        desc
    }
}
export function bool(desc?: Description): Type {
    return {
        ts: "boolean",
        py: "bool",
        desc
    }
}