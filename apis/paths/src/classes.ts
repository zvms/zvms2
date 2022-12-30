import { $ } from "zvms-apis-paths-gen";
import { authData as a } from "zvms-apis-users-data"
import { arr, int, str } from "zvms-apis-types-data";

export const classes = $(
    "/classes",
    [a.abc, a.abc],
    $(
        "/list",
        [a.abc],
        {
            method: "GET",
            desc: "获取班级列表",//Postscript: name随年份自动计算
            req: {
            },
            res: {
                // class:arr(obj(
                //     ["id",int()],
                //     ["name",str()]
                // ))
            },
            _res: {
                class: [
                    { id: 202001, name: "高一1班" },
                    { id: 202011, name: "蛟一1班" },
                    { id: 202002, name: "高一2班" },
                    { id: 201901, name: "高二1班" },
                    { id: 201801, name: "高三1班" }
                ]
            }
        }
    )
);