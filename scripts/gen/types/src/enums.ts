import { snake2Camal } from "zvms-scripts-utils";
import { Type } from "./types";

export type EnumRaw<T> = Record<string, T> & { _type: Type, _pyEnumType?: string };

export type EnumsRaw<T> = Record<string, EnumRaw<T>>;

export type Enums<T, Raw> = Record<keyof Raw, Type & {
    tsDef: string,
    pyDef: string,
    raw: EnumRaw<T>
}>;

export function createEnums<T, Raw extends EnumsRaw<T>>(raw: Raw): Enums<T, Raw> {
    let result: Enums<T, Raw> = {} as any;
    for (const name in raw) {
        const enumRaw = raw[name];
        let tsDef = `export enum ${name}{\n`;
        let pyDef = `class ${name}(${enumRaw._pyEnumType || "Enum"}):\n`;
        for (const key in enumRaw) {
            if (key !== "_type"&&key!=="_pyEnumType") {
                const v = enumRaw[key];
                tsDef += `    ${snake2Camal(key.toLowerCase(), true)} = ${v},\n`;
                pyDef += `    ${key}: ${v}\n`;
            }
        }
        tsDef = tsDef + "}";
        result[name] = {
            ts: `enums.${name}`,
            py: enumRaw._type.py,
            ck: enumRaw._type.ck,
            tsDef,
            pyDef,
            raw: enumRaw
        }
    }
    return result;
}

export function enumsDefGenTs(data: Enums<any, any>): string {
    let str = ``;
    for (const name in data) {
        const struct = data[name];
        str += "\n" + struct.tsDef;
    }
    return str;
}

export function enumsDefGenPy(data: Enums<any, any>): string {
    let str = `from enum import *\n\n`;
    for (const name in data) {
        const struct = data[name];
        str += "\n" + struct.pyDef;
    }
    return str;
}