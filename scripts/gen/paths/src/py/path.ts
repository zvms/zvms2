import { Path } from "../types.js";
import { pyViewsGet, pyImplsGet } from "./get.js";
import { pyViewsPost, pyImplsPost } from "./post.js";

export function pyViewsPath(path: string, pathData: Path) {
    let str = "";
    if (pathData.paths) {
        for (let itemName in pathData.paths) {
            let item = pathData.paths[itemName];
            let crtPath = path + itemName;
            str +=
                `${item.desc ? `'''
${item.desc}
'''`: ""}
${pyViewsGet(crtPath, item.get)} 
${pyViewsPost(crtPath, item.post)}
`
            str += pyViewsPath(crtPath, item);
        }
    }
    return str;
}

export function pyImplsPath(path: string, pathData: Path) {
    let str = "";
    if (pathData.paths) {
        for (let itemName in pathData.paths) {
            let item = pathData.paths[itemName];
            let crtPath = path + itemName;
            str +=
                `${item.desc ? `'''
${item.desc}
'''`: ""}
${pyImplsGet(crtPath, item.get)} 
${pyImplsPost(crtPath, item.post)}
`
            str += pyImplsPath(crtPath, item);
        }
    }
    return str;
}