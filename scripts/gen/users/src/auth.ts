import { UserCatagoryList } from "./catagories.js";

export type AuthData = {
    [k: string]: UserCatagoryList;
}

export function authGenTs(data: AuthData) {
    let str = `export const auth = {\n`;
    for (const name in data) {
        str += `\t${name}: ${data[name].reduce((p, c) => p & c.id, 0)},\n`
    }
    str += `}`;
    return str;
}