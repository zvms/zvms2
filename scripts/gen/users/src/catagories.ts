import { number2ByteCode } from "zvms-scripts-utils"
import { camal2Snake } from "zvms-scripts-utils"

export interface UserCatagory {
    id: number, // permanent, unique
    name: string// for display
}
export type UserCatagoriesRaw = {
    [name: string]: UserCatagory
}
export type UserCatagoriesById = {
    [id: number]: UserCatagory
}
export type UserCatagoryList = readonly UserCatagory[];

export type UserCatagories = {
    raw: UserCatagoriesRaw,
    byId: UserCatagoriesById,
    except(...catagory: UserCatagory[]): UserCatagoryList
};

export function createUserCatagories(rawCatagories: UserCatagoriesRaw): UserCatagories {
    let byId: UserCatagoriesById = {};
    for (const ir in rawCatagories) {
        const r = rawCatagories[ir]
        byId[r.id] = r;
    }
    return {
        raw: rawCatagories,
        byId,
        except(...catagory) {
            let res: UserCatagory[] = [];
            for (const ir in rawCatagories) {
                let t = true;
                const r = rawCatagories[ir]
                for (const c of catagory) {
                    if (r.id === c.id) {
                        t = false;
                        break;
                    }
                }
                if (t) {
                    res.push(r);
                }
            }
            return res;
        }
    }
}

export function createUserOrder(...catagories: UserCatagory[]) {
    return {
        over(c: UserCatagory): UserCatagoryList {
            return catagories.slice(catagories.findIndex(v => v.id === c.id) + 1);
        },
        overEqual(c: UserCatagory): UserCatagoryList {
            return catagories.slice(catagories.findIndex(v => v.id === c.id));
        },
        less(c: UserCatagory): UserCatagoryList {
            return catagories.slice(catagories.findIndex(v => v.id === c.id));
        },
        lessEqual(c: UserCatagory): UserCatagoryList {
            return catagories.slice(catagories.findIndex(v => v.id === c.id) + 1);
        }
    }
}

export function catagoriesGenTs({ raw }: UserCatagories) {
    let str = `
export const userCatagories = {
`;
    for (const name in raw) {
        const catagory = raw[name];
        str += `
    ${name}: {
        id: ${catagory.id},
        name: "${catagory.name}",
    },`
    }
    str += `\n}`;
    return str;
}

export function catagoriesGenPy({ raw }: UserCatagories) {
    let str = `from enum import IntFlag\n\n
class UserCatagories(IntFlag):`;
    for (const name in raw) {
        const catagory = raw[name];
        str += `\n    ${camal2Snake(name).toUpperCase()} = ${number2ByteCode(catagory.id, 8)}`
    }

    str += `\n
class UserCatagoriesInfo:`;
    for (const name in raw) {
        const catagory = raw[name];
        str += `\n    ${name} = {
        'id': ${catagory.id},
        'name': '${catagory.name}',
    }`;
    }
    str += `
    @staticmethod
    def byId(id):
        _data = {`;
    for (const name in raw) {
        const catagory = raw[name];
        str += `
            UserCatagories.${camal2Snake(name).toUpperCase()}: {
                'id': ${catagory.id},
                'name': '${catagory.name}',
            },`;
    }
    str+=`
        }
        return _data[id]`
    return str + "\n";
}