import { Method } from "../types.js";
import { path2LCamal, pyReq2paramsDecl, pyResType, pyComments } from "./utils.js";

export function pyViewsPost(partName: string, path: string, post?: Method) {
    const crtItemPath = path;
    if (post !== undefined) {
        return `
route_post(
    rule='${crtItemPath}',
    impl_func=zvms.impls.${partName}.${post.name},
    params=Object(id=Int, pwd=String),
    auth=${post.auths}
)`
    } else {
        return "";
    }
}

export function pyImplsPost(partName: string, path: string, post?: Method) {
    const crtItemPath = path;
    if (post !== undefined) {
        const decl = pyReq2paramsDecl(post.req);
        const res = pyResType(path2LCamal(crtItemPath), post.res);
        return `
# [POST] ${crtItemPath}
def ${post.name}(${decl})\
 -> ${res.name} : '''
${pyComments(post)}
'''`
    } else {
        return "";
    }
}