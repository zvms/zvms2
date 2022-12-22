import { Part, ImplFiles } from "../types.js";
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

export function genImplsPy(name: string, part: Part, implFiles: ImplFiles): string {
    let str = pyImplsAddBeforeFile;
    str += pyImplsPath(name, part);
    str += pyImplsAddAfterFile;
    return str;
}