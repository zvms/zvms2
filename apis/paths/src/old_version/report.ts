import { Part } from "zvms-apis-paths-gen";
import { arr, str } from "zvms-apis-types-data";
export const report: Part = {
    desc: "反馈",
    paths: {
        items: { //  /report/items/
            get: { // GET --
                desc: "获取反馈列表",
                req:{
                    param1:arr(arr(str())),
                    param2:str()
                },
                res: {
                    data:arr(str())
                }
            },
            post:{

            },
            paths:{
                "123/456":{ //   /report/items/123/456
                    
                }
            }
        },
        "":{ //   /report/

        }
    }
};