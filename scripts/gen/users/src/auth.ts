import { UserCatagoryList } from "./catagories.js";

export type AuthData = Record<string, UserCatagoryList>;

function rjust(str: string, n: number, chr?: string) {
    chr = chr || '0'
    if (str.length > n)
        return str;
    return (chr.repeat(n) + str).slice(-1 * n);
}

export function authGenTs(data: AuthData) {
    let str = `export const auth = {\n`;
    for (const name in data) {
        str += `\t${name}: ${data[name].reduce((p, c) => p & c.id, 0)},\n`
    }
    str += `}`;
    return str;
}

export function authGenPy(data: AuthData) {
    let str = `from enum import IntFlag

class AUTH(IntFlag):`;
    for (const name in data) {
        str += `\n    ${name} = 0b${rjust(data[name].reduce((p, c) => p & c.id, 0).toString(2),8,"0")},`
    }
    return str.slice(0,-1) + "\n";
}