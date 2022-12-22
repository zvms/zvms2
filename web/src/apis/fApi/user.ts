import { get, post } from "./utils";
import * as structs from "../types/structs";

/**
 * ## POST user/login
 * 登陆
 * @param userid
 * @param password
 * @param version
 */
function postUserLogin(
  userid: number,
  password: string,
  version: string
): Promise<{
  username: string;
  classId: number;
  permission: string;
  token: string;
}> {
  return post("user/login", {
    userid,
    password,
    version,
  });
}

/**
 * ## GET user/logout
 * 登出

 */
function getUserLogout(): Promise<{}> {
  return get("user/logout", {});
}

/**
 * ## GET user/info
 * 查看当前登陆账号的信息

 */
function getUserInfo(): Promise<{
  username: string;
  classId: number;
  permission: string;
}> {
  return get("user/info", {});
}

/**
 * ## GET user/getInfo/<userId>
 * 查看账号信息

 */
function getUserGetInfoByUserId(): Promise<{
  username: string;
  classId: number;
  permission: string;
}> {
  return get("user/getInfo/<userId>", {});
}

/**
 * ## POST user/modPwd
 * 修改帐号密码
 * @param oldPwd
 * @param newPwd
 */
function postUserModPwd(oldPwd: string, newPwd: string): Promise<{}> {
  return post("user/modPwd", {
    oldPwd,
    newPwd,
  });
}
