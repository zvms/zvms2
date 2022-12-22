import { Part } from "zvms-apis-paths-gen";
import { arr, int, str, structs } from "zvms-apis-types-data";
export const student: Part = {
    desc: "学生相关",
    paths: {
        "/volbook/<stuId>": {
            get: {
                desc: "查询某个学生的义工本",
                req:{
                },
                res: {
                    rec:arr(structs.VolunteerRecord)
                },
                _res:{
                    "rec": [
                        {"volId": 1, "name": "Event1", "inside": 0.5, "outside": 0, "large": 0, "status": 1},
                        {"volId": 3, "name": "Event2", "inside": 1.5, "outside": 0, "large": 0, "status": 1},
                        {"volId": 5, "name": "Event3", "inside": 0, "outside": 0, "large": 2, "status": 1},
                        {"volId": 6, "name": "Event4", "inside": 0, "outside": 2, "large": 0, "status": 1},
                    ]
                }
            }
        }
    }
};