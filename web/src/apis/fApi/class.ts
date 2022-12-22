import { get, post } from "./utils";
import * as structs from "../types/structs";

/**
 * ## GET class/list
 * 获取班级列表

 */
function getClassList(): Promise<{}> {
  return get("class/list", {});
}

/**
 * ## GET class/stulist/<classId>
 * 获取某个班级的学生列表

 */
function getClassStulistByClassId(): Promise<{}> {
  return get("class/stulist/<classId>", {});
}

/**
 * ## GET class/volunteer/<classId>
 * 查询某个班级能参加的义工活动列表

 */
function getClassVolunteerByClassId(): Promise<{}> {
  return get("class/volunteer/<classId>", {});
}

/**
 * ## GET class/noThought
 * 获取未填写感想的义工

 */
function getClassNoThought(): Promise<{}> {
  return get("class/noThought", {});
}
