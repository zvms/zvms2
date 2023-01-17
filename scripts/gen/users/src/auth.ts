import { number2ByteCode } from "zvms-scripts-utils";
import { UserCatagoryList } from "./catagories.js";

export type AuthData = Record<string, UserCatagoryList>;

export function authGenTs(data: AuthData) {
    let str = `export const authData = {\n`;
    for (const name in data) {
        str += `    ${name}: ${data[name].reduce((p, c) => p | c.id, 0)},\n`
    }
    str += `}`;
    return str;
}

export function authGenPy(data: AuthData) {
    let str = `\n
class AuthData:`;
    for (const name in data) {
        str += `\n    ${name} = ${number2ByteCode(
            data[name].reduce(
                (p, c) => p | c.id
                , 0), 8)}`
    }
    return str.slice(0, -1) + "\n";
}