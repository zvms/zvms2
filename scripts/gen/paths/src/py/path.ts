import { PathItem, GenCtx, ImplCodes } from "../types.js";
import { pyViewsMethod, pyImplsMethod } from "./method.js";

export function pyViewsPath(ctx: GenCtx, pathData: PathItem): string {
    const oldPath = ctx.path;
    ctx.path += pathData.name;
    const result =
        (pathData.methods?.map(
            m => pyViewsMethod(ctx, m)
        )?.join("\n") || "")
        + (pathData.children?.map(
            c => pyViewsPath(ctx, c)
        )?.join("\n") || "");
    ctx.path = oldPath;
    return result;
}

export function pyImplsPath(ctx: GenCtx, pathData: PathItem, implCodes: ImplCodes): string {
    const oldPath = ctx.path;
    ctx.path += pathData.name;
    const result =
        (pathData.methods?.map(
            m => pyImplsMethod(ctx, m, implCodes)
        )?.join("\n") || "")
        + (pathData.children?.map(
            c => pyImplsPath(ctx, c, implCodes)
        )?.join("\n") || "");
    ctx.path = oldPath;
    return result;
}