import { toasts } from "@/utils/dialogs";
import { useLoadingStore } from "@/stores";
import { type AxiosResponse } from "axios";
import axios from "@/plugins/axios";
import * as structs from "./types/structs";
import * as enums from "./types/enums";

function toURLSearchParams(
  kwargs?: any //Record<string, number | string | undefined>
): string {
  if (!kwargs) return "";
  const params: Record<string, string> = {};
  for (const k in kwargs) {
    const v = kwargs[k];
    if (v !== undefined && v !== null) {
      params[k] = v.toString();
    }
  }
  return new URLSearchParams(params).toString();
}

interface ForegroundApiConfig {
  beforeReq(info: ReqInfo): void;
  errorReq(e: Error, info: ReqInfo): void;

  successedRes(res: AxiosResponse<any>, info: ReqInfo): void;
  failedRes(res: AxiosResponse<any> | undefined, info: ReqInfo): void;

  afterProcess(info: ReqInfo): void;
  errorProcess(e: Error, info: ReqInfo): void;

  cleanup(info: ReqInfo): void;

  defaultFailedToast: boolean;
  defaultOkToast: boolean;
}

interface ReqInfo {
  url: string;
  method: MethodType;
  id: number;
}

let _reqId = 0;

export type MethodType = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

export type ForegroundApiProcessor<R extends any> = (
  result: R
) => Promise<void> | void;
export type ForegroundApiRunner<R extends any> = (
  processor?: ForegroundApiProcessor<R>
) => Promise<void>;
export function createForegroundApiRunner<T extends any[], R extends any>(
  fApi: ForegroundApi,
  method: MethodType,
  url: string,
  ...args: T
): ForegroundApiRunner<R> {
  const config = fApi.config;

  const info = {
    url,
    method,
    id: _reqId++,
  };

  const methods = {
    POST: axios.post,
    GET: axios.get,
    DELETE: axios.delete,
    PUT: axios.put,
    PATCH: axios.patch,
  } as const;

  const func = methods[method];
  if (!func) {
    config.errorReq(new Error(`Method ${method} is not supported`), info);
  }

  return async (processor: ForegroundApiProcessor<R> = () => {}) => {
    config.beforeReq(info);
    try {
      let res;
      try {
        res = await func(url, ...args); //axios
      } catch (e:any) {
        if (config.defaultFailedToast) {
          if (e?.code === "ERR_NETWORK") {
            toasts.error("服务器内部错误！");
          } else {
            toasts.error((e as Error).message);
          }
        }
        config.errorReq(e as Error, info);
        throw e;
      }

      if (res?.data?.type !== "SUCCESS") {
        config.failedRes(res, info);
        if (config.defaultFailedToast) {
          toasts.error(res?.data?.message);
        }
      } else {
        const { message, result } = res?.data;
        config.successedRes(res, info);
        try {
          await processor(result);
          if (config.defaultOkToast) {
            toasts.success(message);
          }
          config.afterProcess(info);
        } catch (e) {
          config.errorProcess(e as Error, info);
        }
        config.afterProcess(info);
      }
    } finally {
      config.cleanup(info);
    }
  };
}

export class ForegroundApi {
  config: ForegroundApiConfig;

  constructor(config: ForegroundApiConfig) {
    this.config = config;
  }

  get skipOkToast(): ForegroundApi {
    return new ForegroundApi({
      ...this.config,
      defaultOkToast: false,
    });
  }

  get loadingState(): ForegroundApi {
    const oldConfig: ForegroundApiConfig = this.config;
    return new ForegroundApi({
      ...oldConfig,
      beforeReq(info) {
        oldConfig.beforeReq(info);
        useLoadingStore().incLoading();
      },
      cleanup(info) {
        oldConfig.cleanup(info);
        useLoadingStore().decLoading();
      },
    });
  }

  //--METHODS START----
  /**
   * ## 检查登录状态
   * ### [GET] /user/check
   * #### 权限: Any
   */
  check(): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(this, "GET", `/user/check`);
  }
  /**
   * ## 登录
   * ### [POST] /user/login
   * #### 权限: None
   * @param id
   * @param pwd
   */
  login(
    id: number,
    pwd: string
  ): ForegroundApiRunner<structs.UserLoginResponse> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/user/login`, {
              id,
      pwd
      }
    );
  }
  /**
   * ## 登出
   * ### [POST] /user/logout
   * #### 权限: Any
   */
  logout(): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(this, "POST", `/user/logout`);
  }
  /**
   * ## 搜索用户
   * ### [GET] /user/search
   * #### 权限: Any
   * @param kwargs
   */
  searchUsers(
    kwargs: structs.SearchUsers
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "GET",
      `/user/search?`+ toURLSearchParams(      kwargs)
    );
  }
  /**
   * ## 获取一个用户的详细详细信息
   * ### [GET] /user/<int:id>
   * #### 权限: Any
   * @param id
   */
  getUserInfo(
    id: number
  ): ForegroundApiRunner<structs.UserInfoResponse> {
    return createForegroundApiRunner(
      this,
      "GET",
      `/user/${id}?`+ toURLSearchParams()
    );
  }
  /**
   * ## 获取一个用户(学生)的义工分
   * ### [GET] /user/<int:id>/time
   * #### 权限: Any
   * @param id
   */
  getStudentStat(
    id: number
  ): ForegroundApiRunner<structs.StudentStatResponse> {
    return createForegroundApiRunner(
      this,
      "GET",
      `/user/${id}/time?`+ toURLSearchParams()
    );
  }
  /**
   * ## 修改自己的密码
   * ### [POST] /user/mod-pwd
   * #### 权限: Any
   * @param old
   * @param neo
   */
  modifyPassword(
    old: string,
    neo: string
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/user/mod-pwd`, {
              old,
      neo
      }
    );
  }
  /**
   * ## 创建用户
   * ### [POST] /user/create
   * #### 权限: System
   * @param users
   */
  createUser(
    users: Array<structs.OneUser>
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/user/create`, {
              users
      }
    );
  }
  /**
   * ## 修改用户信息
   * ### [POST] /user/<int:id>/modify
   * #### 权限: System
   * @param id
   * @param name
   * @param cls
   * @param auth
   */
  modifyUser(
    id: number,
    name: string,
    cls: number,
    auth: number
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/user/${id}/modify`, {
              name,
      cls,
      auth
      }
    );
  }
  /**
   * ## 删除用户
   * ### [POST] /user/<int:id>/delete
   * #### 权限: System
   * @param id
   */
  deleteUser(
    id: number
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/user/${id}/delete`, {
        
      }
    );
  }
  /**
   * ## 发送反馈
   * ### [POST] /report
   * #### 权限: Any
   * @param report
   */
  report(
    report: string
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/report`, {
              report
      }
    );
  }
  /**
   * ## 搜索通知
   * ### [GET] /notice/search
   * #### 权限: Any
   * @param kwargs
   */
  searchNotices(
    kwargs: structs.SearchNotices
  ): ForegroundApiRunner<Array<structs.SingleNotice>> {
    return createForegroundApiRunner(
      this,
      "GET",
      `/notice/search?`+ toURLSearchParams(      kwargs)
    );
  }
  /**
   * ## 发送用户通知
   * ### [POST] /notice/send/user
   * #### 权限: Manager | Teacher
   * @param targets
   * @param title
   * @param content
   * @param deadtime
   */
  sendUserNotice(
    targets: Array<number>,
    title: string,
    content: string,
    deadtime: string
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/notice/send/user`, {
              targets,
      title,
      content,
      deadtime
      }
    );
  }
  /**
   * ## 发送班级通知
   * ### [POST] /notice/send/class
   * #### 权限: Manager | Teacher
   * @param targets
   * @param title
   * @param content
   * @param deadtime
   */
  sendClassNotice(
    targets: Array<number>,
    title: string,
    content: string,
    deadtime: string
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/notice/send/class`, {
              targets,
      title,
      content,
      deadtime
      }
    );
  }
  /**
   * ## 发送学校通知
   * ### [POST] /notice/send/school
   * #### 权限: Manager | Teacher
   * @param title
   * @param content
   * @param deadtime
   */
  sendSchoolNotice(
    title: string,
    content: string,
    deadtime: string
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/notice/send/school`, {
              title,
      content,
      deadtime
      }
    );
  }
  /**
   * ## 删除一个通知
   * ### [POST] /notice/<int:id>/delete
   * #### 权限: Manager | Teacher
   * @param id
   */
  deleteNotice(
    id: number
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/notice/${id}/delete`, {
        
      }
    );
  }
  /**
   * ## 修改一个通知
   * ### [POST] /notice/<int:id>/modify
   * #### 权限: Manager | Teacher
   * @param id
   * @param title
   * @param content
   * @param deadtime
   */
  modifyNotice(
    id: number,
    title: string,
    content: string,
    deadtime: string
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/notice/${id}/modify`, {
              title,
      content,
      deadtime
      }
    );
  }
  /**
   * ## 列出一个班级的报名
   * ### [GET] /signup/list/<int:cls>
   * #### 权限: Any
   * @param cls
   */
  listSignup(
    cls: number
  ): ForegroundApiRunner<Array<structs.SingleSignup>> {
    return createForegroundApiRunner(
      this,
      "GET",
      `/signup/list/${cls}?`+ toURLSearchParams()
    );
  }
  /**
   * ## 审核一个报名
   * ### [POST] /signup/<int:volId>/<int:stuId>/audit
   * #### 权限: Class | Teacher
   * @param volId
   * @param stuId
   */
  auditSignup(
    volId: number,
    stuId: number
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/signup/${volId}/${stuId}/audit`, {
        
      }
    );
  }
  /**
   * ## 报名一个义工
   * ### [POST] /signup/<int:volId>
   * #### 权限: Any
   * @param volId
   * @param students
   */
  signup(
    volId: number,
    students: Array<number>
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/signup/${volId}`, {
              students
      }
    );
  }
  /**
   * ## 撤回一个报名
   * ### [POST] /signup/<int:volId>/<int:stuId>/rollback
   * #### 权限: Any
   * @param volId
   * @param stuId
   */
  rollback(
    volId: number,
    stuId: number
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/signup/${volId}/${stuId}/rollback`, {
        
      }
    );
  }
  /**
   * ## 搜索义工
   * ### [GET] /volunteer/search
   * #### 权限: Any
   * @param kwargs
   */
  searchVolunteers(
    kwargs: structs.SearchVolunteers
  ): ForegroundApiRunner<Array<structs.SingleVolunteer>> {
    return createForegroundApiRunner(
      this,
      "GET",
      `/volunteer/search?`+ toURLSearchParams(      kwargs)
    );
  }
  /**
   * ## 获取一个义工的详细信息
   * ### [GET] /volunteer/<int:id>
   * #### 权限: Any
   * @param id
   */
  getVolunteerInfo(
    id: number
  ): ForegroundApiRunner<structs.VolunteerInfoResponse> {
    return createForegroundApiRunner(
      this,
      "GET",
      `/volunteer/${id}?`+ toURLSearchParams()
    );
  }
  /**
   * ## 创建一个义工
   * ### [POST] /volunteer/create
   * #### 权限: Any
   * @param classes
   * @param name
   * @param description
   * @param time
   * @param type
   * @param reward
   */
  createVolunteer(
    classes: Array<structs.ClassVol>,
    name: string,
    description: string,
    time: string,
    type: enums.VolType,
    reward: number
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/volunteer/create`, {
              classes,
      name,
      description,
      time,
      type,
      reward
      }
    );
  }
  /**
   * ## 创建一个成员全部指定的义工
   * ### [POST] /volunteer/create/appointed
   * #### 权限: Any
   * @param joiners
   * @param name
   * @param description
   * @param time
   * @param type
   * @param reward
   */
  createAppointedVolunteer(
    joiners: Array<number>,
    name: string,
    description: string,
    time: string,
    type: enums.VolType,
    reward: number
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/volunteer/create/appointed`, {
              joiners,
      name,
      description,
      time,
      type,
      reward
      }
    );
  }
  /**
   * ## 修改义工
   * ### [POST] /volunteer/<int:id>/modify
   * #### 权限: Any
   * @param id
   * @param classes
   * @param name
   * @param description
   * @param time
   * @param type
   * @param reward
   */
  modifyVolunteer(
    id: number,
    classes: Array<structs.ClassVol>,
    name: string,
    description: string,
    time: string,
    type: enums.VolType,
    reward: number
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/volunteer/${id}/modify`, {
              classes,
      name,
      description,
      time,
      type,
      reward
      }
    );
  }
  /**
   * ## 删除义工
   * ### [POST] /volunteer/<int:id>/delete
   * #### 权限: Any
   * @param id
   */
  deleteVolunteer(
    id: number
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/volunteer/${id}/delete`, {
        
      }
    );
  }
  /**
   * ## 审核义工(班内)
   * ### [POST] /volunteer/<int:id>/audit
   * #### 权限: Class | Teacher
   * @param id
   */
  auditVolunteer(
    id: number
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/volunteer/${id}/audit`, {
        
      }
    );
  }
  /**
   * ## 获取某个学生的感想
   * ### [GET] /thought/student/<int:id>
   * #### 权限: Any
   * @param id
   */
  getStudentThoughts(
    id: number
  ): ForegroundApiRunner<structs.StudentThoughtsResponse> {
    return createForegroundApiRunner(
      this,
      "GET",
      `/thought/student/${id}?`+ toURLSearchParams()
    );
  }
  /**
   * ## 搜索感想
   * ### [GET] /thought/search
   * #### 权限: Any
   * @param kwargs
   */
  searchThoughts(
    kwargs: structs.SearchThoughts
  ): ForegroundApiRunner<Array<structs.SingleThought>> {
    return createForegroundApiRunner(
      this,
      "GET",
      `/thought/search?`+ toURLSearchParams(      kwargs)
    );
  }
  /**
   * ## 获取一个感想的详细信息
   * ### [GET] /thought/<int:volId>/<int:stuId>
   * #### 权限: Any
   * @param volId
   * @param stuId
   */
  getThoughtInfo(
    volId: number,
    stuId: number
  ): ForegroundApiRunner<structs.ThoughtInfoResponse> {
    return createForegroundApiRunner(
      this,
      "GET",
      `/thought/${volId}/${stuId}?`+ toURLSearchParams()
    );
  }
  /**
   * ## 保存感想草稿
   * ### [POST] /thought/<int:volId>/<int:stuId>/save
   * #### 权限: Any
   * @param volId
   * @param stuId
   * @param thought
   * @param pictures
   */
  saveThought(
    volId: number,
    stuId: number,
    thought: string,
    pictures: Array<structs.Picture>
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/thought/${volId}/${stuId}/save`, {
              thought,
      pictures
      }
    );
  }
  /**
   * ## 提交感想
   * ### [POST] /thought/<int:volId>/<int:stuId>/submit
   * #### 权限: Any
   * @param volId
   * @param stuId
   * @param thought
   * @param pictures
   */
  submitThought(
    volId: number,
    stuId: number,
    thought: string,
    pictures: Array<structs.Picture>
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/thought/${volId}/${stuId}/submit`, {
              thought,
      pictures
      }
    );
  }
  /**
   * ## 初审感想(班内)
   * ### [POST] /thought/<int:volId>/<int:stuId>/audit/first
   * #### 权限: Class | Teacher
   * @param volId
   * @param stuId
   */
  firstAudit(
    volId: number,
    stuId: number
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/thought/${volId}/${stuId}/audit/first`, {
        
      }
    );
  }
  /**
   * ## 终审感想(义管会)
   * ### [POST] /thought/<int:volId>/<int:stuId>/audit/final
   * #### 权限: Auditor
   * @param volId
   * @param stuId
   * @param reward
   */
  finalAudit(
    volId: number,
    stuId: number,
    reward: number
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/thought/${volId}/${stuId}/audit/final`, {
              reward
      }
    );
  }
  /**
   * ## 打回感想
   * ### [POST] /thought/<int:volId>/<int:stuId>/repulse
   * #### 权限: Any
   * @param volId
   * @param stuId
   * @param reason
   */
  repulse(
    volId: number,
    stuId: number,
    reason: string
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/thought/${volId}/${stuId}/repulse`, {
              reason
      }
    );
  }
  /**
   * ## 列出所有班级
   * ### [GET] /class/list
   * #### 权限: Any
   */
  listClasses(): ForegroundApiRunner<Array<structs.SingleClass>> {
    return createForegroundApiRunner(this, "GET", `/class/list`);
  }
  /**
   * ## 获取一个班级的详细信息
   * ### [GET] /class/<int:id>
   * #### 权限: Any
   * @param id
   */
  getClassInfo(
    id: number
  ): ForegroundApiRunner<structs.ClassInfoResponse> {
    return createForegroundApiRunner(
      this,
      "GET",
      `/class/${id}?`+ toURLSearchParams()
    );
  }
  /**
   * ## 删除一个班级
   * ### [POST] /class/<int:id>/delete
   * #### 权限: System
   * @param id
   */
  deleteClass(
    id: number
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/class/${id}/delete`, {
        
      }
    );
  }
  /**
   * ## 创建一个班级
   * ### [POST] /class/create
   * #### 权限: System
   * @param name
   */
  createClass(
    name: string
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/class/create`, {
              name
      }
    );
  }
  /**
   * ## 修改一个班级的名称
   * ### [POST] /class/<int:id>/modify
   * #### 权限: System
   * @param id
   * @param name
   */
  modifyClass(
    id: number,
    name: string
  ): ForegroundApiRunner<{}> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/class/${id}/modify`, {
              name
      }
    );
  }


//--METHODS END----

}

export const fApi = new ForegroundApi({
  beforeReq(info: ReqInfo) {},
  errorReq(e: Error, info: ReqInfo) {},

  successedRes(res: AxiosResponse<any>, info: ReqInfo) {},
  failedRes(res: AxiosResponse<any> | undefined, info: ReqInfo) {},

  afterProcess(info: ReqInfo) {},
  errorProcess(e: Error, info: ReqInfo) {},

  cleanup(info: ReqInfo) {},

  defaultFailedToast: true,
  defaultOkToast: true,
}).loadingState;
