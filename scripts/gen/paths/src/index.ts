import { genImplsPy, genViewsPy } from "./py/gen.js";
import { genTs } from "./ts/gen.js";
import { ImplFiles, Apis } from "./types.js";

export * from "./types.js";
export * from "./rawCodes.js";
export { genViewsPy, genImplsPy } from "./py/gen.js";
export { genTs } from "./ts/gen.js";

export type PathsGenerated = { name: string, fApi: string, views: string, impls: string }[];
export function pathsGen(apis: Apis, implFiles: ImplFiles): PathsGenerated {
    const result: PathsGenerated = [];
    for (const part of apis) {
        console.log("Generating", part.name);
        result.push({
            name: part.name.slice(1),
            fApi: genTs(part),
            views: genViewsPy(part),
            impls: genImplsPy(part, implFiles[part.name.slice(1)])
        });
    }
    return result;
}