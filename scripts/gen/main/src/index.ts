import pathsData from "zvms-apis-data/paths";
import { structs as structsData, enums as enumsData } from "zvms-apis-data/types";
import { authData, userCatagories } from "zvms-apis-data/users";
import { fApiIndexRaw, ImplFiles, implsInitRaw, pathsGen, viewsInitRaw } from "zvms-apis-paths-gen";
import { enumsDefGenPy, enumsDefGenTs, structsDefGenCk, structsDefGenPy, structsDefGenTs, typesIndexRaw } from "zvms-apis-types-gen";
import { authGenPy, authGenTs, catagoriesGenPy, catagoriesGenTs, usersIndexRaw } from "zvms-apis-users-gen";
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
    const fileList = fs.readdirSync(paths.b.impls);
    for (const file of fileList) {
        implFiles[file] = fs.readFileSync(join(paths.b.impls, file));
    }

    todos.push(...pathsGen(pathsData, implFiles).map(
        ({ name, fApi, views, impls }) => (
            () => {
                fs.writeFileSync(join(paths.f.fApi, name + ".ts"), prettierTs(fApi));
                fs.writeFileSync(join(paths.b.views, name + ".py"), views);
                fs.writeFileSync(join(paths.b.impls, name + ".py"), impls);
            }
        )
    ));
    todos.push(() => {
        fs.writeFileSync(join(paths.f.fApi, "index.ts"), fApiIndexRaw(pathsData));
        fs.writeFileSync(join(paths.b.views, "__init__.py"), viewsInitRaw(pathsData));
        fs.writeFileSync(join(paths.b.impls, "__init__.py"), implsInitRaw(pathsData));
    });

    todos.push(() => {
        fs.writeFileSync(join(paths.f.users, "catagories.ts"), prettierTs(catagoriesGenTs(userCatagories)));
        fs.writeFileSync(join(paths.b.users, "catagories.py"), catagoriesGenPy(userCatagories));
        fs.writeFileSync(join(paths.f.users, "auth.ts"), prettierTs(authGenTs(authData)));
        fs.writeFileSync(join(paths.b.users, "auth.py"), authGenPy(authData));
        fs.writeFileSync(join(paths.f.users, "index.ts"), usersIndexRaw);
    })

    todos.push(() => {
        fs.writeFileSync(join(paths.f.types, "enums.ts"), prettierTs(enumsDefGenTs(enumsData)));
        fs.writeFileSync(join(paths.b.types, "enums.py"), enumsDefGenPy(enumsData));
        fs.writeFileSync(join(paths.f.types, "structs.ts"), prettierTs(structsDefGenTs(structsData)));
        fs.writeFileSync(join(paths.b.types, "structs.py"), structsDefGenPy(structsData));
        fs.writeFileSync(join(paths.b.types, "structs_ck.py"), structsDefGenCk(structsData));
        fs.writeFileSync(join(paths.f.types, "index.ts"), typesIndexRaw);
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
    return format(str, { parser: "typescript" });
}