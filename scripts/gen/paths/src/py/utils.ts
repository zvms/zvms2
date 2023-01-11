import { Method, Params } from "../types.js";
import { paramName } from "../commonUtils.js";

export * from "../commonUtils.js";

export function pyReq2paramsDecl(req?: Params): string {
    if (!req) return "";
    let ks: string[] = [];
    for (const k in req) {
        ks.push(paramName(k) + ": " + req[k].py);
    }
    return ks.join(",\n");
}

export function pyParamsTypeCheck(req?: Params): string {
    if (!req) return "Object()";
    let result: string[] = [];
    for (const k in req) {
        result.push(req[k].ck);
    }
    return `utils.Object(${result.join(", ")})`;
}

// export function pyResType(apiName: string, res?: Params) {
//     if (!res) return { decl: "", name: "None" };
//     let members: string[] = [];
//     for (const k in res) {
//         members.push(`"${paramName(k)}": ${res[k].py}`);
//     }
//     let typeName = apiName + "Response";
//     return {
//         decl: `${typeName} = TypedDict('${typeName}',
//             {
//                 ${members.join(",\n")}
//             }
//         )`,
//         name: typeName
//     };
// }

export function pyComments(m: Method) {
    if (m.desc && m.desc !== "") {
        return `'''
    ${m.desc            .replaceAll("\n", "\n    ")}
    '''\n`;
    } else {
        return "";
    }
}

export function pyCommentStr(comment?: string) {
    return comment ?
        `# ${comment}\n` :
        "\n";
}