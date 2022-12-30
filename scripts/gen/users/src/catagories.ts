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

let a = [1 as any as UserCatagory,
1 as any as UserCatagory] as const as UserCatagoryList

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
    },\n`
    }
    str += `\n}`;
    return str;
}

function toSnackUppercase(str: string) {
    let result = "";
    for (const c of str) {
        if (65 <= c.charCodeAt(0) && c.charCodeAt(0) <= 90) {
            result += "_";
        }
        result += c;
    }
    return result.toUpperCase();
}

export function catagoriesGenPy({ raw }: UserCatagories) {
    let str = `\n`;
    for (const name in raw) {
        const catagory = raw[name];
        str += `
${toSnackUppercase(name)} = {
    'id': ${catagory.id},
    'name': '${catagory.name}',
},\n`
    }
    return str;
}