import { get, post } from "./utils";
import * as structs from "../types/structs";

/**
 * ## GET student/volbook/<stuId>
 * 查询某个学生的义工本

 */
function getStudentVolbookByStuId(): Promise<{
  rec: Array<structs.VolunteerRecord>;
}> {
  return get("student/volbook/<stuId>", {});
}
