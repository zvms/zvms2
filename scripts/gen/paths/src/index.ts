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
    for (const partName in apis) {
        const part = (apis)[partName];
        result.push({
            name: partName,
            fApi: genTs(partName, part),
            views: genViewsPy(partName, part),
            impls: genImplsPy(partName, part, implFiles)
        })
    }
    return result;
}