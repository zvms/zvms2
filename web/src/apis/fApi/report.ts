import { get, post } from "./utils";
import * as structs from "../types/structs";

/**
 * ## GET reportitems
 * 获取反馈列表
 * @param param1
 * @param param2
 */
function getReportitems(
  param1: Array<Array<string>>,
  param2: string
): Promise<{
  data: Array<string>;
}> {
  return get("reportitems", {
    param1,
    param2,
  });
}

/**
 * ## POST reportitems
 
 */
function postReportitems(): undefined {
  return post("reportitems", {});
}
