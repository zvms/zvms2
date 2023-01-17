import pathsData from "zvms-apis-data/paths";
import { structs as structsData, enums as enumsData } from "zvms-apis-data/types";
import { authData, userCatagories } from "zvms-apis-data/users";
import { ImplFiles, implsInitRaw, pathsGen, viewsInitRaw } from "zvms-apis-paths-gen";
import { enumsDefGenPy, enumsDefGenTs, structsDefGenCk, structsDefGenPy, structsDefGenTs } from "zvms-apis-types-gen";
import { authGenPy, authGenTs, catagoriesGenPy, catagoriesGenTs } from "zvms-apis-users-gen";
import zvmsConfig from "zvms-config";

import * as fs from "./fs.js";

import { join } from "node:path";
import { format } from "prettier";

const { paths } = zvmsConfig;

export function main(output: boolean) {
    const todos = generate();
    backup();
    if (output) apply(todos);
    else console.log("Outputing is closed.")
}

function generate(): (() => void)[] {
    let todos: (() => void)[] = [];

    let implFiles: ImplFiles = {};
    // const fileList = fs.readdirSync(paths.b.impls);
    // for (const file of fileList) {
    //     implFiles[file] = fs.readFileSync(join(paths.b.impls, file));
    // }

    let fApiTemplate = fs.readFileSync(join(paths.f.fApi, "fApi-template.ts"));

    const pathsGenerated = pathsGen(pathsData, implFiles, fApiTemplate);
    todos.push(...pathsGenerated.files.map(
        ({ name, views/*, impls*/ }) => (
            () => {
                fs.writeFileSync(join(paths.b.views, name + ".py"), views);
                //fs.writeFileSync(join(paths.b.impls, name + ".py"), impls);
            }
        )
    ));
    const fApiOpt = prettierTs(pathsGenerated.fApi),
        viewsInitOpt = viewsInitRaw(pathsData),
        implsInitOpt = implsInitRaw(pathsData);
    todos.push(() => {
        fs.writeFileSync(join(paths.f.fApi, "fApi.ts"), fApiOpt);
        fs.writeFileSync(join(paths.b.views, "__init__.py"), viewsInitOpt);
        //fs.writeFileSync(join(paths.b.impls, "__init__.py"), implsInitOpt);
    });

    const catagoriesTsOpt = prettierTs(catagoriesGenTs(userCatagories)),
        catagoriesPyOpt = catagoriesGenPy(userCatagories),
        authTsOpt = prettierTs(authGenTs(authData)),
        authPyOpt = authGenPy(authData);
    todos.push(() => {
        fs.writeFileSync(join(paths.f.users, "catagories.ts"), catagoriesTsOpt);
        fs.writeFileSync(join(paths.b.users, "catagories.py"), catagoriesPyOpt);
        fs.writeFileSync(join(paths.f.users, "auth.ts"), authTsOpt);
        fs.writeFileSync(join(paths.b.users, "auth.py"), authPyOpt);
    })

    const enumsTsOpt = prettierTs(enumsDefGenTs(enumsData)),
        enumsPyOpt = enumsDefGenPy(enumsData),
        structsTsOpt = prettierTs(structsDefGenTs(structsData)),
        structsPyOpt = structsDefGenPy(structsData),
        structsCkOpt = structsDefGenCk(structsData);
    todos.push(() => {
        fs.writeFileSync(join(paths.f.types, "enums.ts"), enumsTsOpt);
        fs.writeFileSync(join(paths.b.types, "enums.py"), enumsPyOpt);
        fs.writeFileSync(join(paths.f.types, "structs.ts"), structsTsOpt);
        fs.writeFileSync(join(paths.b.types, "structs.py"), structsPyOpt);
        fs.writeFileSync(join(paths.b.types, "structs_ck.py"), structsCkOpt);
    })

    return todos;
}

function backup() {
    const backupPath = join(paths.backup, `${Date.now()}`);
    fs.mkdirSync(backupPath);
    const backupList = [
        [paths.f.fApi, "f-fApi"],
        [paths.b.views, "b-views"],
        [paths.b.impls, "b-impls"],
        [paths.f.users, "f-users"],
        [paths.f.types, "f-types"],
        [paths.b.res, "b-res"]
    ];
    for (const item of backupList) {
        fs.cpSync(item[0], join(backupPath, item[1]), { recursive: true });
    }
}

function apply(todos: (() => void)[]) {
    todos.forEach(v => v());
}

function prettierTs(str: string) {
    try {
        return format(str, { parser: "typescript" });
    } catch (e) {
        console.error(e, str);
        return str;
    }
}