import { Path } from "../types.js";
import { pyViewsGet, pyImplsGet } from "./get.js";
import { pyViewsPost, pyImplsPost } from "./post.js";

export function pyViewsPath(partName: string, path: string, pathData: Path) {
    let str = "";
    if (pathData.paths) {
        for (let itemName in pathData.paths) {
            let item = pathData.paths[itemName];
            let crtPath = path + itemName;
            str +=
                `${item.desc ? `'''
${item.desc}
'''`: ""}
${pyViewsGet(partName, crtPath, item.get)} 
${pyViewsPost(partName, crtPath, item.post)}
`
            str += pyViewsPath(partName, crtPath, item);
        }
    }
    return str;
}

export function pyImplsPath(partName: string, path: string, pathData: Path) {
    let str = "";
    if (pathData.paths) {
        for (let itemName in pathData.paths) {
            let item = pathData.paths[itemName];
            let crtPath = path + itemName;
            str +=
                `${item.desc ? `'''
${item.desc}
'''`: ""}
${pyImplsGet(partName, crtPath, item.get)} 
${pyImplsPost(partName, crtPath, item.post)}
`
            str += pyImplsPath(partName, crtPath, item);
        }
    }
    return str;
}