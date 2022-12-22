import { isTimeFinished, timeToHint } from "../../utils/calc.js";
import { toasts } from "../../utils/dialogs";


export class ForegroundApi {

    async fetchClassList() {
        //let res = await this.get("/class/list");
        return [{ "id": 202001, "name": "高一1班" },
        { "id": 202011, "name": "蛟一1班" },
        { "id": 202002, "name": "高一2班" },
        { "id": 201901, "name": "高二1班" },
        { "id": 201801, "name": "高三1班" }];
    }

    async fetchStudentList(classid) {
        let student = [
            { "id": classid + "01", "name": "王可", "inside": 1.5, "outside": 2, "large": 8 },
            { "id": classid + "02", "name": "王不可", "inside": 2.5, "outside": 2, "large": 8 },
            { "id": classid + "03", "name": "王可以", "inside": 5, "outside": 8, "large": 0 },
            { "id": classid + "04", "name": "王不行", "inside": 1, "outside": 4, "large": 16 },
            { "id": classid + "05", "name": "王彳亍", "inside": 5, "outside": 0, "large": 8 }
        ]

        for (let stu of student) {
            stu.finished = isTimeFinished(stu.id, stu) ? "是" : "否";
        }

        return student;
    }

    async fetchClassVolunter(classid) {
        let volunteer = classid ? [
            { "id": 1, "name": "义工活动1", "date": "2020.10.1", "time": "13:00", "description": "Description\nDescription\nDescription", "status": 1, "stuMax": 20 },
            { "id": 2, "name": "义工活动2", "date": "2020.10.2", "time": "13:00", "description": "Description\nDescription\nDescription", "status": 1, "stuMax": 2 },
            { "id": 3, "name": "义工活动3", "date": "2020.10.3", "time": "13:00", "description": "Description\nDescription\nDescription", "status": 0, "stuMax": 5 },
            { "id": 4, "name": "义工活动4", "date": "2020.10.4", "time": "13:00", "description": "Description\nDescription\nDescription", "status": 2, "stuMax": 10 }
        ] : [
            { "id": 1, "name": "义工活动1", "description": "Description\nDescription\nDescription", "date": "2020.10.1", "time": "13:00", "status": 1, "stuMax": 20 },
            { "id": 2, "name": "义工活动2", "description": "Description\nDescription\nDescription", "date": "2020.10.2", "time": "13:00", "status": 1, "stuMax": 2 },
            { "id": 3, "name": "义工活动3", "description": "Description\nDescription\nDescription", "date": "2020.10.3", "time": "13:00", "status": 0, "stuMax": 5 },
            { "id": 4, "name": "义工活动4", "description": "Description\nDescription\nDescription", "date": "2020.10.4", "time": "13:00", "status": 2, "stuMax": 10 }
        ];

        return volunteer;
    }

    async fetchAllVolunter() {
        //let res = await this.get("/volunteer/list")
        return [
            { "id": 1, "name": "义工活动1", "description": "Description\nDescription\nDescription", "date": "2020.10.1", "time": "13:00", "status": 1, "stuMax": 20 },
            { "id": 2, "name": "义工活动2", "description": "Description\nDescription\nDescription", "date": "2020.10.2", "time": "13:00", "status": 1, "stuMax": 2 },
            { "id": 3, "name": "义工活动3", "description": "Description\nDescription\nDescription", "date": "2020.10.3", "time": "13:00", "status": 0, "stuMax": 5 },
            { "id": 4, "name": "义工活动4", "description": "Description\nDescription\nDescription", "date": "2020.10.4", "time": "13:00", "status": 2, "stuMax": 10 }
        ]
    }

    async fetchOneVolunteer() {
        //let res = await this.get("/volunteer/fetch/" + id)
        return {
            "type": "SUCCESS",
            "message": "获取成功",
            "name": "义工活动1",
            "date": "2020.10.1",
            "time": "13:00",
            "stuMax": 20,
            "stuNow": 18,
            "description": "Description\nDescription\nDescription",
            "status": 1,
            "inside": 0,
            "outside": 3,
            "large": 0
        };
    }

    async fetchUnauditedVolunteers() {
        return [
            { "volId": 1, "stuId": 20200101, "thought": "xxxx" },
            { "volId": 3, "stuId": 20200102, "thought": "xxxx" }
        ];
    }

    async fetchSignerList() {
        //let res = await this.get("/volunteer/signerList/" + volid,)
        return [
            { "stuId": 20200101, "stuName": "王彳亍" },
            { "stuId": 20200102, "stuName": "王不可" },
            { "stuId": 20200103, "stuName": "王可" }
        ];
    }

    async fetchVolbook() {
        let data = {
            "type": "SUCCESS",
            "message": "获取成功",
            "rec": [
                { "volId": 1, "name": "Event1", "inside": 0.5, "outside": 0, "large": 0, "status": 1 },
                { "volId": 3, "name": "Event2", "inside": 1.5, "outside": 0, "large": 0, "status": 1 },
                { "volId": 5, "name": "Event3", "inside": 0, "outside": 0, "large": 2, "status": 1 },
                { "volId": 6, "name": "Event4", "inside": 0, "outside": 2, "large": 0, "status": 1 },
            ]
        }
        let volworks = data.rec.map(v => ({
            ...v,
            inside: timeToHint(v.inside),
            outside: timeToHint(v.outside),
            large: timeToHint(v.large),
        }));
        return volworks;
    }

    async fetchNothoughtList() {
        return [
            { "volId": 1, "stuId": 20200101 },
            { "volId": 3, "stuId": 20200102 }
        ];
    }

    async openPictures(callback) {
        getIpcRenderer().once("open-picture-recv", (_, data) => {
            callback(data)
        })
        getIpcRenderer().send("open-picture")
    }

    async openCSV(callback) {
        getIpcRenderer().once("open-csv-recv", (_, data) => {
            callback(data)
        })

        getIpcRenderer().send("open-csv")
    }

    async fetchNotices() {
        return [
            {
                title: "1",
                text: "1111"
            },
            {
                title: "2",
                text: "2222"
            }
        ];
    }

    async sendNotice() {
        // let res = await this.post("/user/sendNotice", {
        //     target,
        //     title,
        //     deadtime,
        //     message
        // })
        // return res.data
    }

    async sendReport() {
        // let res = await this.post("/report", {
        //     report: msg
        // })
        // return res.data;
    }

    async volcert() {
        return {
            vol:123,
            stu:456,
        }
    }

    async login() {
        return {
            "type": "SUCCESS",
            "message": "登陆成功",
            "username": "Admin",
            "class": 202001,
            "permission": 10,
            "token": "xxxx"
        };
    }

    async modifyPwd() {
        return {
            "type": "SUCCESS",
            "message": "修改成功"
        };
    }

    async audit() {
        return {
            "type": "SUCCESS",
            "message": "提交成功"
        };
    }

    async createVol() {
        return {
            "type": "SUCCESS",
            "message": "创建成功"
        };
    }

    async submitHolidayVol() {
        return {
            "type": "SUCCESS",
            "message": "创建成功"
        };
    }
}

export const fApi = new ForegroundApi(
    (e, _func, ...args) => {
        toasts.error(`"${e}" (URL: "${args[0]}")`);
        // console.error(
        //     `Error on request. Args ${args.join(",")}`, e
        // )
        throw new Error(e)
    },
    (res) => {
        toasts.error(res.data.message);
    },
    () => {
        store.commit("incLoading");
    },
    () => {
        store.commit("decLoading");
    }
)