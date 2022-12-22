import * as fs from "node:fs";
import { join } from "node:path";

export function toRoot(path: string) {
    return join(process.cwd(), "../../", path);
}

export function cpSync(source: string, destination: string, opts?: fs.CopySyncOptions) {
    return fs.cpSync(toRoot(source), toRoot(destination), opts);
}

export function mkdirSync(path: string) {
    return fs.mkdirSync(toRoot(path), { recursive: true });
}

export function writeFileSync(file: string, data: string) {
    return fs.writeFileSync(toRoot(file), data);
}