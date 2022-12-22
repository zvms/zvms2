import { Type } from "./types.js";

export type StructRaw = Record<string, Type>;

export type StructsRaw = Record<string, StructRaw>;

export type Structs<Raw> = Record<keyof Raw, Type & { tsDef: string, pyDef: string }>;

export function structsDefGenTs(data: Structs<any>): string {
    let str = ``;
    for (const name in data) {
        const struct = data[name];
        str += struct.tsDef;
    }
    return str
}

export function createStructs<Raw extends StructsRaw>(raw: Raw): Structs<Raw> {
    let result: Structs<Raw> = {} as any;
    for (const name in raw) {
        const struct = raw[name];
        let tsDef = `export interface ${name}{\n`;
        let pyDef = `${name} = TypedDict('${name}',{`;
        for (const key in struct) {
            const type = struct[key];
            tsDef += `\t${key}:${type.ts};\n`;
            pyDef += `\t'${key}':${type.py},\n`;
        }
        tsDef += "}\n";
        pyDef += "})\n";
        result[name] = {
            tsDef: tsDef,
            pyDef: pyDef,
            ts: `structs.${name}`,
            py: `structs.${name}`,
        }
    }
    return result;
}