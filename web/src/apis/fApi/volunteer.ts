import { get, post } from "./utils";
import * as structs from "../types/structs";

/**
 * ## GET volunteer/list
 * 义工活动总表

 */
function getVolunteerList(): Promise<{}> {
  return get("volunteer/list", {});
}

/**
 * ## GET volunteer/fetch/<volId>
 * 查询单次义工详细信息

 */
function getVolunteerFetchByVolId(): Promise<{
  name: string;
  date: string;
  time: string;
  stuMax: number;
  stuNow: number;
  description: string;
  status: number;
  inside: number;
  outside: number;
  large: number;
}> {
  return get("volunteer/fetch/<volId>", {});
}

/**
 * ## POST volunteer/signup/<volId>
 * 报名义工活动
 * @param stulist
 */
function postVolunteerSignupByVolId(stulist: Array<number>): Promise<{}> {
  return post("volunteer/signup/<volId>", {
    stulist,
  });
}

/**
 * ## POST volunteer/create
 * 创建义工活动
 * @param name
 * @param date
 * @param time
 * @param stuMax
 * @param description
 * @param status
 * @param inside
 * @param outside
 * @param large
 */
function postVolunteerCreate(
  name: string,
  date: string,
  time: string,
  stuMax: number,
  description: string,
  status: number,
  inside: number,
  outside: number,
  large: number
): Promise<{}> {
  return post("volunteer/create", {
    name,
    date,
    time,
    stuMax,
    description,
    status,
    inside,
    outside,
    large,
  });
}

/**
 * ## GET volunteer/signerList/<volId>
 * 获取义工活动报名列表

 */
function getVolunteerSignerListByVolId(): Promise<{}> {
  return get("volunteer/signerList/<volId>", {});
}

/**
 * ## POST volunteer/thought/<volId>
  * 义工活动感想提交

 */
function postVolunteerThoughtByVolId(): Promise<{}> {
  return post("volunteer/thought/<volId>", {});
}

/**
 * ## GET volunteer/randomThought
 * 随机获取一条感想
 * @param username
 * @param userId
 * @param content
 */
function getVolunteerRandomThought(
  username: string,
  userId: number,
  content: string
): Promise<{}> {
  return get("volunteer/randomThought", {
    username,
    userId,
    content,
  });
}

/**
 * ## POST volunteer/audit/<volId>
 * 感想审核
 * @param thought
 */
function postVolunteerAuditByVolId(
  thought: Array<structs.VolunteerRecord>
): Promise<{}> {
  return post("volunteer/audit/<volId>", {
    thought,
  });
}

/**
 * ## GET volunteer/unaudited
 * 获取未审核感想

 */
function getVolunteerUnaudited(): Promise<{}> {
  return get("volunteer/unaudited", {});
}

/**
 * ## POST volunteer/holiday
 * 假期义工统一修改
 * @param name
 * @param date
 * @param time
 * @param stuId
 * @param description
 * @param inside
 * @param outside
 * @param large
 */
function postVolunteerHoliday(
  name: string,
  date: string,
  time: string,
  stuId: Array<number>,
  description: string,
  inside: number,
  outside: number,
  large: number
): Promise<{}> {
  return post("volunteer/holiday", {
    name,
    date,
    time,
    stuId,
    description,
    inside,
    outside,
    large,
  });
}
