import { PathItem, ImplFile, ImplCodes } from "../types.js";
import { pyViewsPath, pyImplsPath } from "./path.js";

const pyViewsAddBeforeFile = `from zvms.routelib import *
from zvms.res import *
import zvms.impls as impls
`;
const pyViewsAddAfterFile = "";

export function genViewsPy(part: PathItem): string {
    let str = pyViewsAddBeforeFile;
    str += pyViewsPath({
        fileName: part.name.slice(1),
        path: ""
    }, part);
    str += pyViewsAddAfterFile;
    return str;
}

const pyImplsAddBeforeFile = `import typing

from zvms.models import *
from zvms.res import *
from zvms.utils import *

`;
const pyImplsAddAfterFile = "";

export function genImplsPy(part: PathItem, implFile: ImplFile): string {
    // console.log(implFile?.slice(0, 50));
    // let results =
    //     /# *\[GET\] ([\w/<>:]+)\ndef (\w+)\([\w, :\*]*\)(-> \w+ )?:\n(    \'\'\'[\s\S]*?\'\'\')?/gm
    //         .exec(implFile)
    // console.log(results);

    // if (results !== null) {
    //     results[0]
    // }
    let matched = implFile.matchAll(
        /(?<=^|#\s*\[([A-Z]+)\]\s*([\w/<:>]+)\ndef\s*\w+\(.*?\)\s*(\->\w\s*)?\s*:(\n\s*'''.*?''')?).*?(?=$|\n#\s*\[[A-Z]+\]\s*([\w/<:>]+)\ndef\s*\w+\(.*?\))/gs
    );
    let implCodes: ImplCodes = {};
    let isBeginning = true, beginning = "";
    for (const m of matched) {
        if (isBeginning) {
            isBeginning = false;
            if (m[1] === undefined && m[2] === undefined) {
                beginning = m[0];
            } else {
                implCodes[m[1] + " " + m[2]] = [m[0], false];
            }
        } else {
            implCodes[m[1] + " " + m[2]] = [m[0], false];
        }
    }
    let str = pyImplsAddBeforeFile;
    str += pyImplsPath({
        fileName: part.name.slice(1),
        path: ""
    }, part, implCodes);
    str += pyImplsAddAfterFile;

    for (const k in implCodes) {
        if (!implCodes[k][1]) {
            console.error("WARNING: unused implCode!");
            console.error("    - file:  ", part.name);
            console.error("    - method:", k);
        }
    }
    return str;
}