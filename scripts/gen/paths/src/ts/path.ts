import { Path } from "../types.js";
import { tsGet } from "./get.js";
import { tsPost } from "./post.js";

export function tsPath(path: string, pathData: Path) {
    let str = "";
    if (pathData.paths) {
        for (let itemName in pathData.paths) {
            let item = pathData.paths[itemName];
            let crtPath = path + itemName;
            str +=
                `${item.desc ? `/**
 * ${item.desc}
 */`: ""}
${tsGet(crtPath, item.get)} 
${tsPost(crtPath, item.post)}
`
            str += tsPath(crtPath, item);
        }
    }
    return str;
}