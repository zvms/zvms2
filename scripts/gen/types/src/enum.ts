
export type EnumRaw<T> = Record<string, T>;

export type EnumsRaw<T> = Record<string, EnumRaw<T>>;

export type Enums<T, Raw> = Record<keyof Raw, {
    tsDef: string,
    pyDef: string,
    raw: EnumRaw<T>
}>;

export function createEnums<T, Raw extends EnumsRaw<T>>(raw: Raw): Enums<T, Raw> {
    let result: Enums<T, Raw> = {} as any;
    for (const name in raw) {
        const enumRaw = raw[name];
        let tsDef = `export enum ${name}{\n`;
        let pyDef = `class ${name}(Enum):\n`;
        for (const key in enumRaw) {
            const v = enumRaw[key];
            tsDef += `    ${key}= ${v},\n`;
            pyDef += `    ${key}: ${v}\n`;
        }
        tsDef = tsDef + "}";
        result[name] = {
            tsDef,
            pyDef,
            raw: enumRaw
        }
    }
    return result;
}

export function enumsDefGenTs(data: Enums<any,any>): string {
    let str = ``;
    for (const name in data) {
        const struct = data[name];
        str += "\n" + struct.tsDef;
    }
    return str;
}

export function enumsDefGenPy(data: Enums<any,any>): string {
    let str = `from enum import Enum\n\n`;
    for (const name in data) {
        const struct = data[name];
        str += "\n" + struct.pyDef;
    }
    return str + "\n";
}