import { Method } from "../types.js";
import { path2LCamal, req2paramsApply, tsReq2paramsDecl, tsResType, tsComments } from "./utils.js";

export function tsGet(path: string, get?: Method) {
    const crtItemPath = path;
    if (get !== undefined) {
        const decl = tsReq2paramsDecl(get.req);
        return `
/**
 * ## GET ${crtItemPath}
${tsComments(get)}
 */
function get${path2LCamal(crtItemPath)}(${decl}): ${tsResType(get.res)} {
\treturn get("${crtItemPath}",{
\t\t${req2paramsApply(get.req)}
\t});
}
`
    } else {
        return "";
    }
}