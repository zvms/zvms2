import { Type, Description } from "./types.js";

export function arr(type: Type, desc?: Description): Type {
    return {
        ts: `Array<${type.ts}>`,
        py: `typing.Sequence[${type.py}]`,
        ck: `Array(${type.ck})`,
        desc
    }
}
export function str(desc?: Description): Type {
    return {
        ts: "string",
        py: "str",
        ck: "String",
        desc
    }
}
export function strMaxLength(max: number, desc?: Description): Type {
    return {
        ts: "string",
        py: "str",
        ck: `String(${max})`,
        desc
    }
}
export function int(desc?: Description): Type {
    return {
        ts: "number",
        py: "int",
        ck: "Int",
        desc
    }
}
export function float(desc?: Description): Type {
    return {
        ts: "number",
        py: "float",
        ck: "Float",
        desc
    }
}
export function bool(desc?: Description): Type {
    return {
        ts: "boolean",
        py: "bool",
        ck: "Boolean",
        desc
    }
}
export function any(desc?: Description): Type {
    return {
        ts: `any`,
        py: `typing.Any`,
        ck: `Any`,
        desc
    }
}
export interface LiteralValuedType {
    literal: {
        ts: string,
        py: string,
        ck: string,
    }
}
export function literal(...values: LiteralValuedType[]) {
    return {
        ts: values.map(v => v.literal.ts).join(" | "),
        py: values.map(v => v.literal.py).join(" | "),
        ck: "Literal(" + values.map(v => v.literal.ck).join(", ") + ")",
    }
}