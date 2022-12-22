import { isTimeFinished, timeToHint } from "../utils/calc.js";
import { toasts } from "../utils/dialogs";
import { useLoadingStore } from "../stores";
import Axios from "axios";


export class ForegroundApi {
    _id = 1;

    constructor(
        requestError,
        notSuccess,
        beforeRequest,
        afterRequest) {
        this.requestError = requestError;
        this.notSuccess = notSuccess;
        this.beforeRequest = beforeRequest;
        this.afterRequest = afterRequest;
    }
    requestError;
    notSuccess;
    beforeRequest;
    afterRequest;

    async doRequest(func, ...args) {
        let cid = this._id++;
        this.beforeRequest(cid, ...args);
        let res = await func(...args).catch(
            (e) => this.requestError(e, func, ...args)
        ).finally(
            this.afterRequest(cid, ...args)
        );
        if (res.data.type !== "SUCCESS") {
            this.notSuccess(res);
        }
        return res;
    }

    post(url, data, config) {
        return this.doRequest(Axios.post, url, data, config);
    }

    get(url, config) {
        return this.doRequest(Axios.get, url, config);
    }

    async fetchClassList() {
        let res = await this.get("/class/list");
        return res.data.class;
    }

    async fetchStudentList(classid) {
        let res = await this.get("/class/stulist/" + classid);

        for (let stu of res.data.student) {
            stu.finished = isTimeFinished(stu.id, stu) ? "是" : "否";
        }
        return res.data.student;
    }

    async fetchClassVolunter(classid) {
        let url = classid ? "/class/volunteer/" + classid : "/volunteer/list/";
        let res = await this.get(url)
        return res.data.volunteer;
    }

    async fetchAllVolunter() {
        let res = await this.get("/volunteer/list")
        return res.data.volunteer
    }

    async fetchOneVolunteer(id) {
        let res = await this.get("/volunteer/fetch/" + id)
        return res.data;
    }

    async fetchUnauditedVolunteers() {
        let res = await this.get("/volunteer/unaudited")
        return res.data.result;
    }

    async fetchSignerList(volid) {
        let res = await this.get("/volunteer/signerList/" + volid,)
        return res.data.result;
    }

    async fetchVolbook(id) {
        let res = await this.get("/student/volbook/" + id)

        //     if (response.data.message != "该学生没有义工记录")
        //       toasts.error(response.data.message);
        //   } TODO

        let volworks = res.data.rec.map(v => ({
            inside: timeToHint(v.inside),
            outside: timeToHint(v.outside),
            large: timeToHint(v.large),
        }));
        return volworks;
    }

    async fetchNothoughtList(cls) {
        let res = await this.get("/class/noThought/" + cls)
        return res.data.result;
    }

    async openPictures(callback) {
        (()=>{throw new Error("IpcRenderer Removed!")},undefined)
    }

    async openCSV(callback) {
        getIpcRenderer().once("open-csv-recv", (_, data) => {
            callback(data)
        })

        getIpcRenderer().send("open-csv")
    }

    async fetchNotices() {
        let res = await this.get("/user/notices");
        return res.data;
    }

    async sendNotice(target, title, deadtime, message) {
        let res = await this.post("/user/sendNotice", {
            target,
            title,
            deadtime,
            message
        })
        return res.data
    }

    async sendReport(msg) {
        let res = await this.post("/report", {
            report: msg
        })
        return res.data;
    }

    async volcert(volid, stuid) {
        let res = await this.post("/student/volcert/", {
            volId: volid,
            stuId: stuid
        });
        return res.data
    }

    async login(userid, passwdMD5, version) {
        let res = await this.post("/user/login", {
            "userid": userid,
            "password": passwdMD5,
            "version": version
        })
        return res.data;
    }

    async modifyPwd(oldMD5, newMD5) {
        let res = await this.post("/user/modPwd", {
            "oldPwd": oldMD5,
            "newPwd": newMD5
        });
        return res.data;
    }

    async audit(volid, stuid, status, inside, outside, large) {
        let res = await this.post("/volunteer/audit/" + volid, {
            "thought": [{
                "stuId": stuid,
                "status": status,
                "inside": inside,
                "outside": outside,
                "large": large
            }]
        })
        return res.data;
    }

    async createVol(
        name,
        date,
        time,
        stuMax,
        description,
        inside,
        outside,
        large, classSelected) {
        let res = await this.post("/volunteer/create", {
            name,
            date,
            time,
            stuMax: parseInt(stuMax),
            description,
            inside: parseInt(inside),
            outside: parseInt(outside),
            large: parseInt(large),
            class: classSelected,
        })
        return res.data;
    }

    async submitHolidayVol(name,
        date,
        time,
        stuId,
        description,
        inside,
        outside,
        large) {
        let res = await this.post("/volunteer/holiday", {
            name,
            date,
            time,
            stuId,
            description,
            inside,
            outside,
            large
        })
        return res;
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
        useLoadingStore().incLoading();
    },
    () => {
        useLoadingStore().decLoading();
    }
)