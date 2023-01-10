import { snake2Camal } from "zvms-scripts-utils";

import { GenCtx, Method } from "../types.js";
import { req2paramsApply, tsReq2paramsDecl, tsResType, tsComments } from "./utils.js";

export function tsMethod(ctx: GenCtx, method: Method) {
    const decl = tsReq2paramsDecl(method.req);
    return `/**
 * ## [${method.type.toUpperCase()}] ${ctx.path}
 ${tsComments(method)}
 */
export function ${snake2Camal(method.name)}(${decl}): ${tsResType(method.res)} {
    return ${method.type.toLowerCase()}("${ctx.path}", {
        ${req2paramsApply(method.req)}
    });
}`;
}