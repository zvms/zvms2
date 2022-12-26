import { Part } from "zvms-apis-paths-gen";
import { arr, int, str } from "zvms-apis-types-data";
export const class2: Part = {
    desc: "班级相关",
    paths: {
        "/list": {
            get: {
                desc: "获取班级列表",//Postscript: name随年份自动计算
                req:{
                },
                res: {
                    // class:arr(obj(
                    //     ["id",int()],
                    //     ["name",str()]
                    // ))
                },
                _res:{
                    class:[
                        {id: 202001, name: "高一1班"},
                        {id: 202011, name: "蛟一1班"},
                        {id: 202002, name: "高一2班"},
                        {id: 201901, name: "高二1班"},
                        {id: 201801, name: "高三1班"}
                    ]
                }
            }
        },
        "/stulist/<classId>": {
            get: {
                desc: "获取某个班级的学生列表",
                req:{
                },
                res: {
                    // student:arr(obj(
                    //     ["id",int()],
                    //     ["name",str()],
                    //     ["inside",int()],
                    //     ["outside",int()],
                    //     ["large",int()]
                    // ))
                },
                _res:{
                    student:[
                        {id: 20200101, name: "王可", inside: 1.5, outside: 2, large: 8},
                        {id: 20200102, name: "王不可", inside: 2.5, outside: 2, large: 8},
                        {id: 20200103, name: "王可以", inside: 5, outside: 8, large: 0},
                        {id: 20200104, name: "王不行", inside: 1, outside: 4, large: 16},
                        {id: 20200105, name: "王彳亍", inside: 5, outside: 0, large: 8}
                    ]
                }
            }
        },
        "/volunteer/<classId>": {
            get: {
                desc: "查询某个班级能参加的义工活动列表",
                req:{
                },
                res: {
                    // volunteer:arr(obj(
                    //     ["id",int()],
                    //     ["name",str()],
                    //     ["date",str()],
                    //     ["time",str()],
                    //     ["description",str()],
                    //     ["status",int()],
                    //     ["stuMax",int()]
                    // ))
                },
                _res:{
                    volunteer: [
                        {id: 1, name: "义工活动1", date: "2020.10.1", time: "13:00", description: "...", status: 1, stuMax: 20},
                        {id: 2, name: "义工活动2", date: "2020.10.2", time: "13:00", description: "...", status: 1, stuMax: 2},
                        {id: 3, name: "义工活动3", date: "2020.10.3", time: "13:00", description: "...", status: 0, stuMax: 5},
                        {id: 4, name: "义工活动4", date: "2020.10.4", time: "13:00", description: "...", status: 2, stuMax: 10}
                    ]
                }
            }
        },
        "/noThought": {
            get: {
                desc: "获取未填写感想的义工",
                req:{                    
                },
                res:{
                    // result:arr(obj(
                    //     ["volId",int()],
                    //     ["stuId",int()]
                    // ))
                },
                _res:{
                    result:[
                        {volId:1,stuId:20200101},
                        {volId:3,stuId:20200102}
                    ]
                }
            }
        }
    }
};