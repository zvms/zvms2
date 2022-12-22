import { Part } from "zvms-apis-paths-gen";
import { arr, str, int, bool, structs} from "zvms-apis-types-data";
export const volunteer: Part = {
    desc: "义工活动相关",
    paths: {
        "/list": {
            get: {
                desc: "义工活动总表",
                req:{
                },
                res: {
                    // volunteer:arr(obj(
                    //     ["id",int()],
                    //     ["name",str()],
                    //     ["description",str()],
                    //     ["date",str()],
                    //     ["time",str()],
                    //     ["status",int()],
                    //     ["stuMax",int()]
                    // ))
                },
                _res:{
                    "volunteer": [
                        {"id": 1, "name": "义工活动1", "description": "...", "date": "2020.10.1", "time": "13:00", "status": 1, "stuMax": 20},
                        {"id": 2, "name": "义工活动2", "description": "...", "date": "2020.10.2", "time": "13:00", "status": 1, "stuMax": 2},
                        {"id": 3, "name": "义工活动3", "description": "...", "date": "2020.10.3", "time": "13:00", "status": 0, "stuMax": 5},
                        {"id": 4, "name": "义工活动4", "description": "...", "date": "2020.10.4", "time": "13:00", "status": 2, "stuMax": 10}
                    ]
                }
            }
        },
        "/fetch/<volId>": {
            get: {
                desc: "查询单次义工详细信息",
                req:{
                },
                res: {
                    name:str(),
                    date:str(),
                    time:str(),
                    stuMax:int(),
                    stuNow:int(),
                    description:str(),
                    status:int(),
                    inside:int(),
                    outside:int(),
                    large:int()
                },
                _res:{
                    "name": "义工活动1",
                    "date": "2020.10.1",
                    "time": "13:00",
                    "stuMax": 20,
                    "stuNow": 18,
                    "description": "...",
                    "status": 1,
                    "inside": 0,
                    "outside": 3,
                    "large": 0
                }
            }
        },
        "/signup/<volId>": {
            post: {
                desc: "报名义工活动",
                req:{
                    stulist:arr(int())
                },
                res: {
                },
                _req:{
                    "stulst": [
                        20200101,
                        20200102,
                        20200103
                    ]
                }
            }
        },
        "/create": {
            post: {
                desc: "创建义工活动",
                req:{
                    name:str(),
                    date:str(),
                    time:str(),
                    stuMax:int(),
                    description:str(),
                    status:int(),
                    inside:int(),
                    outside:int(),
                    large:int(),
                    // class:arr(obj(
                    //     ["id",int()],
                    //     ["stuMax",int()],
                    //     ["visible",bool()]
                    // ))
                },
                res: {
                },
                _req:{
                    "name": "义工活动1",
                    "date": "2020.10.1",
                    "time": "13:00",
                    "stuMax": 20,
                    "description": "...",
                    "inside": 0,
                    "outside": 3,
                    "large": 0,
                    "class": [
                        {"id": 202001, "stuMax": 10, "visible": true},
                        {"id": 202002, "stuMax": 5, "visible": true},
                        {"id": 202003, "stuMax": 10, "visible": true},
                        {"id": 202004, "stuMax": 0, "visible": false}
                    ]
                }
            }
        },
        "/signerList/<volId>": {
            get: {
                desc: "获取义工活动报名列表",
                req:{        
                },
                res: {
                    // result:arr(obj(
                    //     ["stuId",int()],
                    //     ["stuName",str()]
                    // ))
                },
                _res:{
                    "result": [
                        {"stuId": 20200101, "stuName": "王彳亍"},
                        {"stuId": 20200102, "stuName": "王不可"},
                        {"stuId": 20200103, "stuName": "王可"}
                    ]
                }
            }
        },
        "/thought/<volId>": {
            post: {
                desc: "义工活动感想提交",
                req:{
                    // thought:arr(obj(
                    //     ["stuId",int()],
                    //     ["content",str()]
                    // ))
                },
                res: {
                },
                _req:{
                    "thought":[
                        {"stuId": 20200101, "content": "没有感想"},
                        {"stuId": 20200102, "content": "感想没有"}
                    ]
                }
            }
        },
        "/randomThought": {
            get: {
                desc: "随机获取一条感想",
                req:{
                    username:str(),
                    userId:int(),
                    content:str()
                },
                res: {
                },
                cfg:{
                    token:false
                },
                _req:{
                    "userName": "王彳亍",
                    "userId": 20200101,
                    "content": "没有感想"
                }     
            }
        },
        "/audit/<volId>": {
            post: {
                desc: "感想审核",
                req:{
                    thought:arr(structs.VolunteerRecord)
                },
                res: {
                },
                _req:{
                    "thought": [
                        {"stuId": 20200101, "status": 1, "inside": 70, "outside": 0, "large": 0},
                        {"stuId": 20200102, "status": 2, "inside": 0, "outside": 0, "large": 0},
                        {"stuId": 20200103, "status": 3, "inside": 0, "outside": 0, "large": 0}
                    ]
                }
            }
        },
        "/unaudited": {
            get: {
                desc: "获取未审核感想",
                req:{   
                },
                res: {
                    // result:arr(obj(
                    //     ["volId",int()],
                    //     ["stuId",int()],
                    //     ["thought",str()]
                    // ))
                },
                cfg:{
                    token:false
                },
                _res:{
                    "result": [
                        {"volId": 1, "stuId": 20200101, "thought": "xxxx"},
                        {"volId": 3, "stuId": 20200102, "thought": "xxxx"}
                    ]
                }
            }
        },
        "/holiday": {
            post: {
                desc: "假期义工统一修改",
                req:{
                    name:str(),
                    date:str(),
                    time:str(),
                    stuId:arr(int()),
                    description:str(),
                    inside:int(),
                    outside:int(),
                    large:int()
                },
                res: {
                },
                _req:{
                    "name":"打扫xxxx",
                    "date":"2021.2.30",
                    "time":"12:00",
                    "stuId":[20200101,20200102,20200103],
                    "description":"ftp://ftp/aaa/bbb.docx",
                    "inside":0,
                    "outside":4,
                    "large":2
                }
            }
        }
    }
};