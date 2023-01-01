import { GenCtx, ImplCodes, Method } from "../types.js";
import { pyReq2paramsDecl, pyComments, pyParamsTypeCheck } from "./utils.js";

export function pyViewsMethod(ctx: GenCtx, method: Method) {
        return `
route_${method.type.toLowerCase()}(
    rule='${ctx.path}',
    impl_func=zvms.impls.${ctx.fileName}.${method.name},
    params=${pyParamsTypeCheck(method.req)},
    auth=${method.auths}
)`;
}

export function pyImplsMethod(ctx: GenCtx, method: Method, implCodes: ImplCodes) {
        const decl = pyReq2paramsDecl(method.req);
        let impl = implCodes[method.type.toUpperCase() + " " + ctx.path]
        if (impl === undefined) {
                impl = [`    raise 'Unimplmented!'`, true];
        }
        else {
                impl[1] = true;
        }
        return `
# [${method.type.toUpperCase()}] ${ctx.path}
def ${method.name}(${decl}) -> never : '''
${pyComments(method)}
'''${impl[0]}`
}