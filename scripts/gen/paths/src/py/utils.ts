import { Method, Params } from "../types.js";
import { cfg2str, paramName } from "../commonUtils.js";

export * from "../commonUtils.js";

export function pyReq2paramsDecl(req?: Params): string {
    if (!req) return "";
    let ks: string[] = [];
    for (const k in req) {
        ks.push(paramName(k) + ": " + req[k].py);
    }
    return ks.join(",\n");
}

export function pyReq2paramsDesc(req?: Params): string[] {
    if (!req) return [];
    // let descs: string[] = [];
    // for (const k in req) {
    //     descs.push(` * @param ${paramName(k)} ${req[k].desc || ""}`)
    // }
    // return descs;
    return [];
}

export function pyResType(apiName: string, res?: Params) {
    if (!res) return { decl: "", name: "None" };
    let members: string[] = [];
    for (const k in res) {
        members.push(`"${paramName(k)}": ${res[k].py}`);
    }
    let typeName = apiName + "Response";
    return {
        decl: `${typeName} = TypedDict('${typeName}',
            {
                ${members.join(",\n")}
            }
        )
        `,
        name: typeName
    };
}

export function pyComments(m: Method) {
    return `${pyAddSharp(m.desc)}${pyAddSharp(cfg2str(m.cfg))}${pyReq2paramsDesc(m.req).join("\n")}`
}

export function pyAddSharp(str: string | undefined) {
    return str ? "# " + str + "\n" : "";
}

export function pyCommentStr(comment?: string) {
    return comment ?
        `# ${comment}\n` :
        "\n";
}