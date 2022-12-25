import { Part, ImplFile } from "../types.js";
import { pyViewsPath, pyImplsPath } from "./path.js";

const pyViewsAddBeforeFile = `
import typing
`;
const pyViewsAddAfterFile = "";

export function genViewsPy(name: string, part: Part): string {
    let str = pyViewsAddBeforeFile;
    str += pyViewsPath(name, name, part);
    str += pyViewsAddAfterFile;
    return str;
}

const pyImplsAddBeforeFile = `
import typing
`;
const pyImplsAddAfterFile = "";

export function genImplsPy(name: string, part: Part, implFile: ImplFile): string {
    // console.log(implFile?.slice(0, 50));
    // let results =
    //     /# *\[GET\] ([\w/<>:]+)\ndef (\w+)\([\w, :\*]*\)(-> \w+ )?:\n(    \'\'\'[\s\S]*?\'\'\')?/gm
    //         .exec(implFile)
    // console.log(results);

    // if (results !== null) {
    //     results[0]
    // }

    let methods = "GET|POST|PATCH";
    let matched = implFile.matchAll(
        RegExp(
            `\
(?<=# *\\[${methods}\\] ([\\w/<>:]+)\\n\
def (\\w+)\\([\\w, :\\*]*\\)(-> \\w+ )?:\\n\
(    \\'\\'\\'[\\s\\S]*?\\'\\'\\')?)[\\s\\S]*?\
(?=$|(# *\\[${methods}\\]))`,
            "gm"
        )
    );




    let str = pyImplsAddBeforeFile;
    str += pyImplsPath(name, name, part);
    str += pyImplsAddAfterFile;
    return str;
}