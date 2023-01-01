import { GenCtx, Method } from "../types.js";
import { req2paramsApply, tsReq2paramsDecl, tsResType, tsComments, snack2camal } from "./utils.js";

export function tsMethod(ctx:GenCtx, method: Method) {
        const decl = tsReq2paramsDecl(method.req);
        return `/**
 * ## [${method.type.toUpperCase()}] ${ctx.path}
 ${tsComments(method)}
 */
export function ${snack2camal(method.name)}(${decl}): ${tsResType(method.res)} {
    return ${method.type.toLowerCase()}("${ctx.path}", {
        ${req2paramsApply(method.req)}
    });
}`;
}