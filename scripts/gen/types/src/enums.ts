import { snake2Camal } from "zvms-scripts-utils";
import { LiteralValuedType } from "./common";
import { Type } from "./types";

export type EnumRaw<K extends {}, T> = Record<keyof K, T> & { _type: Type, _pyEnumType?: string };

type EnumKeys<E extends EnumRaw<any, any>> =
    E extends EnumRaw<infer K, any> ? Exclude<keyof K, "_type" | "_pyEnumType"> : never;

export type EnumsRaw<ES extends Record<string, EnumRaw<any, any>>> = {
    [Name in keyof ES]: ES[Name];
};

export type Enums<
    ES extends Record<string, EnumRaw<any, any>>> =
    { [Name in keyof ES]: Type & {
        tsDef: string,
        pyDef: string,
        raw: ES[Name],
        literal: Record<EnumKeys<ES[Name]>, LiteralValuedType>,
    }
    };

export function createEnums<ES extends Record<string, EnumRaw<any, any>>>(raw: EnumsRaw<ES>): Enums<ES> {
    const result: Enums<ES> = {} as any;
    for (const name in raw) {
        const enumRaw = raw[name];
        let literal: {
            [Key in keyof ES[typeof name]]: LiteralValuedType;
        } = {} as any;
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