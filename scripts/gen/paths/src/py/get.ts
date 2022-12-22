import { Method } from "../types.js";
import { path2LCamal, pyReq2paramsDecl, pyResType, pyComments } from "./utils.js";

export function pyViewsGet(path: string, get?: Method) {
    const crtItemPath = path;
    if (get !== undefined) {
        const decl = pyReq2paramsDecl(get.req);
        const res = pyResType(path2LCamal(crtItemPath), get.res);
        return `
${res.decl}
def get${path2LCamal(crtItemPath)}(${decl})\
 -> ${res.name} : '''
## GET ${crtItemPath}
${pyComments(get)}
'''`
    } else {
        return "";
    }
}

export function pyImplsGet(path: string, get?: Method) {
    const crtItemPath = path;
    if (get !== undefined) {
        const decl = pyReq2paramsDecl(get.req);
        const res = pyResType(path2LCamal(crtItemPath), get.res);
        return `
${res.decl}
def get${path2LCamal(crtItemPath)}(${decl})\
 -> ${res.name} : '''
## GET ${crtItemPath}
${pyComments(get)}
'''`
    } else {
        return "";
    }
}