import { genImplsPy, genViewsPy } from "./py/gen.js";
import { genTs } from "./ts/gen.js";
import { ImplFiles, Apis } from "./types.js";

export * from "./types.js";
export * from "./rawCodes.js";
export { genViewsPy, genImplsPy } from "./py/gen.js";
export { genTs } from "./ts/gen.js";

export type PathsGenerated = {
    files: { name: string, views: string, impls: string }[],
    fApi: string
};
export function pathsGen(apis: Apis, implFiles: ImplFiles, fApiTemplate: string): PathsGenerated {
    const result: PathsGenerated = {
        files: [],
        fApi: genTs(apis, fApiTemplate)
    };
    for (const part of apis) {
        console.log("Generating", part.name);
        result.files.push({
            name: part.name.slice(1),
            views: genViewsPy(part),
            impls: ""//genImplsPy(part, implFiles[part.name.slice(1) + ".py"])
        });
    }
    return result;
}