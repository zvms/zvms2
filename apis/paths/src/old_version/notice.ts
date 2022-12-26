import { Part } from "zvms-apis-paths-gen";
import { arr, str, int, structs } from "zvms-apis-types-data";
export const notice: Part = {
    desc: "公告相关",
    paths: {
        "/new": {
            post: {
                desc: "新建一条公告",
                req:{
                    content:str(),
                    announcer:str()
                },
                res: {
                },
                _req:{
                    "content": "blablablablah",
                    "announcer": "20200101 xxx"
                }
            }
        },
        "/query": {
            get: {
                desc: "查询活跃公告",
                req:{
                },
                res: {
                    list:arr(structs.Notice)
                },
                _res:{
                    "list": [
                        {"content": "blablablablah", "announcer": "20200101 xxx", "time": "2020.01.01 00:00:01", "id": 2},
                        {"content": "blablablablah", "announcer": "20200102 xxx", "time": "2020.01.01 00:00:02", "id": 5},
                        {"content": "blablablablah", "announcer": "20200103 xxx", "time": "2020.01.01 11:45:14", "id": 6}
                    ]
                }
            }
        },
        "/modify/<ntcId>": {
            post: {
                desc: "修改指定公告",
                req:{
                    id:int(),
                    content:str(),
                    announcer:str(),
                    time:str(),
                    status:int()
                },
                res: {
                },
                _req:{
                    "id": 5,
                    "content": "blablablablah",
                    "announcer": "20200101 xxx",
                    "time": "2020.01.01 00:00:01",
                    "status": 0
                }
            }
        }
    }
};