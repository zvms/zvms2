import { Part, ImplFile } from "../types.js";
import { pyViewsPath, pyImplsPath } from "./path.js";

const pyViewsAddBeforeFile = `
import typing
`;
const pyViewsAddAfterFile = "";

export function genViewsPy(name: string, part: Part): string {
    let str = pyViewsAddBeforeFile;
    str += pyViewsPath(name, part);
    str += pyViewsAddAfterFile;
    return str;
}

const pyImplsAddBeforeFile = `
import typing
`;
const pyImplsAddAfterFile = "";

export function genImplsPy(name: string, part: Part, implFile: ImplFile): string {
    let results = /# \[GET\] ([\w/]+)\ndef (\w+)\([\w, :\*]*\) (-> \w+ )?: \n    \'\'\'[\s\S]*?\'\'\'/gm
        .exec(implFile)
    console.log(results);

    let str = pyImplsAddBeforeFile;
    str += pyImplsPath(name, part);
    str += pyImplsAddAfterFile;
    return str;
}