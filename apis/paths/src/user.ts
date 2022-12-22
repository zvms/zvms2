import { Part } from "zvms-apis-paths-gen";
import { str, int } from "zvms-apis-types-data";
export const user: Part = {
    desc: "用户相关",
    paths: {
        "/login": {
            post: {
                desc: "登陆",
                req:{
                    userid:int(),
                    password:str(),
                    version:str()
                },
                res:{
                    //may happen a error res (index.md)?
                    username:str(),
                    class:int(),
                    permission:str(),
                    token:str()
                },
                _req:{
                    userid: 202001,   //userid int (index中写str)
                    password: "123456",
                    version: "f63163cdb1493c95a036f8830d0132c5"
                },
                _res:{
                    username:"王彳亍",
                    class: 202001,
                    permission: 0,
                    token: "xxxx"
                },
                cfg: {
                    token: false
                }
            }
        },
        "/logout": {
            get: {
                desc: "登出",
                req: {
                },
                res: {//no example (_)?
                },
                cfg: {
                    token: false
                }
            }
        },
        "/info": {
            get: {
                desc: "查看当前登陆账号的信息",
                req: {
                },
                res: {
                    username:str(),
                    class:int(),
                    permission:str()
                },
                _res:{
                    username: "王彳亍",
                    class: 202001,
                    permission: 0
                }
            }
        },
        "/getInfo/<userId>": {
            get: {
                desc: "查看账号信息",
                req: {
                },
                res: {
                    username:str(),
                    class:int(),
                    permission:str()
                },
                _res:{
                    username:"王彳亍",
                    class:202001,
                    permission:0
                }
            }
        },
        "/modPwd": {
            post: {
                desc: "修改帐号密码",
                req:{
                    oldPwd:str(),
                    newPwd:str()
                },
                res: {
                },
                _req:{
                    oldPwd:"d41d8cd9...",
                    newPwd:"e10adc39..."
                }
            }
        }
    }
};