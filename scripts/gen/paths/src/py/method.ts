import { GenCtx, ImplCodes, Method } from "../types.js";
import { pyReq2paramsDecl, pyComments, pyParamsTypeCheck } from "./utils.js";

export function pyViewsMethod(ctx: GenCtx, method: Method) {
        return `
route_${method.type.toLowerCase()}(
    rule='${ctx.path}',
    impl_func=zvms.impls.${ctx.fileName}.${method.name},
    params=${pyParamsTypeCheck(method.req)},
    auth=${method.auths?.flatMap(v1=>v1.map(v2=>v2.id)).reduce((v1,v2)=>v1&v2,0)||"0b11111111"}
)`;}

export function pyImplsMethod(ctx: GenCtx, method: Method, implCodes: ImplCodes) {
        const decl = pyReq2paramsDecl(method.req);
        let impl = implCodes[method.type.toUpperCase() + " " + ctx.path]
        if (impl === undefined) {
                impl = [`\n    raise 'Unimplmented!'\n`, true];
        }
        else {
                impl[1] = true;
        }
        return `# [${method.type.toUpperCase()}] ${ctx.path}
def ${method.name}(${decl}) -> typing.NoReturn:${pyComments(method)}${impl[0]}`
}