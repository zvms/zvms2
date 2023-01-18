import { snake2Camal } from "zvms-scripts-utils";
import { LiteralValuedType } from "./common";
import { Type } from "./types";

export type EnumRaw<T> = Record<string, T> & { _type: Type, _pyEnumType?: string };

export type EnumsRaw<T> = Record<string, EnumRaw<T>>;

export type Enums<Raw> = Record<keyof Raw, Type & {
    tsDef: string,
    pyDef: string,
    raw: EnumRaw<unknown>,
    literal: Record<string, LiteralValuedType>,
}>;

export function createEnums<T, Raw extends EnumsRaw<T>>(raw: Raw): Enums<Raw> {
    const result: Enums<Raw> = {} as any;
    for (const name in raw) {
        const enumRaw = raw[name];
        let literal: Record<string, LiteralValuedType> = {};
        let tsDef = `export enum ${name}{\n`;
        let pyDef = `class ${name}(${enumRaw._pyEnumType || "Enum"}):\n`;
        for (const key in enumRaw) {
            if (key !== "_type" && key !== "_pyEnumType") {
                const v = enumRaw[key];

                const tsKeyname = snake2Camal(key.toLowerCase(), true),
                    pyKeyName = key;

                tsDef += `    ${tsKeyname} = ${v},\n`;
                pyDef += `    ${pyKeyName} = ${v}\n`;
                literal[key] = {
                    literal: {
                        ts: `enums.${name}.${tsKeyname}`,
                        py: `enums.${name}.${pyKeyName}`,
                        ck: `enums.${name}.${pyKeyName}`,
                    }
                };
            }
        }
        tsDef = tsDef + "}";
        result[name] = {
            ts: `enums.${name}`,
            py: enumRaw._type.py,
            ck: enumRaw._type.ck,
            tsDef,
            pyDef,
            raw: enumRaw,
            literal
        }
    }
    return result;
}

export function enumsDefGenTs(data: Enums<any>): string {
    let str = ``;
    for (const name in data) {
        const struct = data[name];
        str += "\n" + struct.tsDef;
    }
    return str;
}

export function enumsDefGenPy(data: Enums<any>): string {
    let str = `from enum import *\n\n`;
    for (const name in data) {
        const struct = data[name];
        str += "\n" + struct.pyDef;
    }
    return str;
}