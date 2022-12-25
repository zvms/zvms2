import { Method } from "../types.js";
import { path2LCamal, pyReq2paramsDecl, pyResType, pyComments } from "./utils.js";

export function pyViewsGet(partName: string, path: string, get?: Method) {
    const crtItemPath = path;
    if (get !== undefined) {
        return `
route_get(
    rule='${crtItemPath}',
    impl_func=zvms.impls.${partName}.${get.name},
    params=Object(id=Int, pwd=String),
    auth=${get.auths}
)`
    } else {
        return "";
    }
}

export function pyImplsGet(partName: string, path: string, get?: Method) {
    const crtItemPath = path;
    if (get !== undefined) {
        const decl = pyReq2paramsDecl(get.req);
        const res = pyResType(path2LCamal(crtItemPath), get.res);
        return `
# [GET] ${crtItemPath}
def ${get.name}(${decl})\
 -> ${res.name} :
    '''
    ${pyComments(get)}
    '''`
    } else {
        return "";
    }
}