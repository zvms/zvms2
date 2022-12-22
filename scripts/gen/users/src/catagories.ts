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
export type UserCatagoryList = UserCatagory[];

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
            let res: UserCatagoryList = [];
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
        str +=
            `\t${name}: {
\t\tid: ${catagory.id},
\t\tname: "${catagory.name}",
\t},\n`
    }
    str += `
}`;
    return str;
}