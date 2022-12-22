import { Method } from "../types.js";
import { path2LCamal, req2paramsApply, tsReq2paramsDecl, tsResType, tsComments } from "./utils.js";

export function tsPost(path: string, post?: Method) {
    const crtItemPath = path;
    if (post !== undefined) {
        const decl = tsReq2paramsDecl(post.req);
        return `
/**
 * ## POST ${crtItemPath}
 ${tsComments(post)}
 */
function post${path2LCamal(crtItemPath)}(${decl}): ${tsResType(post.res)} {
\treturn post("${crtItemPath}",{
\t\t${req2paramsApply(post.req)}
\t});
}
`
    } else {
        return "";
    }
}