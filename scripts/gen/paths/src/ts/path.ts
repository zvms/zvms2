import { GenCtx, PathItem } from "../types.js";
import { tsMethod } from "./method.js";

export function tsPath(ctx: GenCtx, pathData: PathItem): string {
    let oldPath = ctx.path;
    ctx.path += pathData.name;
    let result =
        (pathData.methods?.map(
            m => tsMethod(ctx, m)
        )?.join("\n") || "")
        + (pathData.children?.map(
            c => tsPath(ctx, c)
        )?.join("\n") || "");
    ctx.path = oldPath;
    return result;
}