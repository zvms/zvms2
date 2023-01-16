import { snake2Camal } from "zvms-scripts-utils";

import { GenCtx, Method } from "../types.js";
import { req2paramsApply, tsReq2paramsDecl, tsResType, tsComments } from "./utils.js";

export function tsMethod(ctx: GenCtx, method: Method) {
    const decl = tsReq2paramsDecl(method.req);
    return `/**
 * ## [${method.type.toUpperCase()}] ${ctx.path}
 ${tsComments(method)}
 */
${snake2Camal(method.name)}(${decl}): ForegroundApiRunner<${tsResType(method.res)}> {
    return createForegroundApiRunner(
        this,
        "${method.type.toUpperCase()}",
        "${ctx.path}",
        ${req2paramsApply(method.req)}
    });
}`;
}