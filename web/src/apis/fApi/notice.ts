import { get, post } from "./utils";
import * as structs from "../types/structs";

/**
 * ## POST notice/new
 * 新建一条公告
 * @param content
 * @param announcer
 */
function postNoticeNew(content: string, announcer: string): Promise<{}> {
  return post("notice/new", {
    content,
    announcer,
  });
}

/**
 * ## GET notice/query
 * 查询活跃公告

 */
function getNoticeQuery(): Promise<{
  list: Array<structs.Notice>;
}> {
  return get("notice/query", {});
}

/**
 * ## POST notice/modify/<ntcId>
 * 修改指定公告
 * @param id
 * @param content
 * @param announcer
 * @param time
 * @param status
 */
function postNoticeModifyByNtcId(
  id: number,
  content: string,
  announcer: string,
  time: string,
  status: number
): Promise<{}> {
  return post("notice/modify/<ntcId>", {
    id,
    content,
    announcer,
    time,
    status,
  });
}
