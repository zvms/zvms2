import { toasts } from "@/utils/dialogs";
import { useLoadingStore } from "@/stores";
import Axios, { type AxiosResponse } from "axios";
import * as structs from "./types/structs";
import * as enums from "./types/enums";

interface ForegroundApiConfig {
  beforeRequest(info: ReqInfo): void;
  afterRequest(info: ReqInfo): void;
  errorRequest(e: Error, info: ReqInfo): void;

  notSuccessed(res: AxiosResponse<any> | undefined, info: ReqInfo): void;
  successed(res: AxiosResponse<any>, info: ReqInfo): void;

  beforeProcess(info: ReqInfo): void;
  afterProcess(info: ReqInfo): void;
  errorProcess(e: Error, info: ReqInfo): void;

  cleanup(info: ReqInfo): void;
}

interface ReqInfo {
  url: string;
  method: MethodType;
  id: number;
}

let _reqId = 0;

export type MethodType = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

export type ForegroundApiProcessor<R extends any[]> = (
  ...args: R
) => Promise<void> | void;
export type ForegroundApiRunner<R extends any[]> = (
  processor: ForegroundApiProcessor<R>
) => Promise<void>;
export function createForegroundApiRunner<T extends any[], R extends any[]>(
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
    POST: Axios.post,
    GET: Axios.get,
    DELETE: Axios.delete,
    PUT: Axios.put,
    PATCH: Axios.patch,
  } as const;

  const func = methods[method];
  if (!func) {
    config.errorRequest(new Error(`Method ${method} is not supported`), info);
  }

  return async (processor: ForegroundApiProcessor<R>) => {
    config.beforeRequest(info);
    try {
      let toProcess = false;
      let res;
      try {
        res = await func(url, ...args);
      } catch (e) {
        config.errorRequest(e as Error, info);
      }

      if (res?.data?.type !== "SUCCESS") {
        config.notSuccessed(res, info);
      } else {
        config.successed(res, info);
        toProcess = true;
      }
      config.afterRequest(info);

      if (toProcess) {
        config.beforeProcess(info);
        try {
          await processor(...(res as unknown as R));
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

  get errorToast(): ForegroundApi {
    return new ForegroundApi({
      ...this.config,
      errorRequest(e, info) {
        this.errorRequest(e, info);
        toasts.error(e.message);
      },
    });
  }

  okToast(msg: string): ForegroundApi {
    return undefined as any;//UNFINISHED
  }

  get loadingState(): ForegroundApi {
    const oldConfig: ForegroundApiConfig = this.config;
    return new ForegroundApi({
      ...oldConfig,
      beforeRequest(info) {
        oldConfig.beforeRequest(info);
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
   * ## 列出所有班级
   * ### [GET] /class/list
   * #### 权限: Any
   */
  listClasses(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", `/class/list`);
  }
  /**
   * ## 获取一个班级的详细详细
   * ### [GET] /class/<int:id>
   * #### 权限: Any
   * @param id
   */
  getClassInfo(id: number): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", `/class/${id}`);
  }
  /**
   * ## 删除一个班级
   * ### [POST] /class/<int:id>/delete
   * #### 权限: System
   * @param id
   */
  deleteClass(id: number): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", `/class/${id}/delete`);
  }
  /**
   * ## 创建一个班级
   * ### [POST] /class/create
   * #### 权限: System
   * @param name
   */
  createClass(
    name: string
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/class/create`,
      name);
  }
  /**
   * ## 修改一个班级的名称
   * ### [POST] /class/<int:id>/modify
   * #### 权限: System
   * @param name
   * @param id
   */
  modifyClass(
    id: number,
    name: string
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/class/${id}/modify`,
      name);
  }
  /**
   * ## 搜索通知
   * ### [GET] /notice/search
   * #### 权限: Any
   * @param sender
   * @param user
   * @param cls
   * @param school
   */
  searchNotices(
    sender?: number,
    user?: number,
    cls?: number,
    school?: any
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "GET",
      `/notice/search`,
      ...Array<any>(
        sender,
        user,
        cls,
        school
      ).filter((value: any) => value != undefined));
  }
  /**
   * ## 发送用户通知
   * ### [POST] /notice/send/user
   * #### 权限: Manager | Teacher
   * @param title
   * @param content
   * @param deadtime
   * @param targets
   */
  sendUserNotice(
    title: string,
    content: string,
    deadtime: string,
    targets: Array<number>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/notice/send/user`,
      title,
      content,
      deadtime,
      targets);
  }
  /**
   * ## 发送班级通知
   * ### [POST] /notice/send/class
   * #### 权限: Manager | Teacher
   * @param title
   * @param content
   * @param deadtime
   * @param targets
   */
  sendClassNotice(
    title: string,
    content: string,
    deadtime: string,
    targets: Array<number>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/notice/send/class`,
      title,
      content,
      deadtime,
      targets);
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
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/notice/send/school`,
      title,
      content,
      deadtime);
  }
  /**
   * ## 删除一个通知
   * ### [POST] /notice/<int:id>/delete
   * #### 权限: Manager | Teacher
   * @param id
   */
  deleteNotice(id: number): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", `/notice/${id}/delete`);
  }
  /**
   * ## 修改一个通知
   * ### [POST] /notice/<int:id>/modify
   * #### 权限: Manager | Teacher
   * @param title
   * @param content
   * @param deadtime
   * @param id
   */
  modifyNotice(
    id: number,
    title: string,
    content: string,
    deadtime: string
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/notice/${id}/modify`,
      title,
      content,
      deadtime);
  }
  /**
   * ## 发送反馈
   * ### [POST] /report
   * #### 权限: Any
   * @param report
   */
  report(
    report: string
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/report`,
      report);
  }
  /**
   * ## 列出一个班级的报名
   * ### [GET] /signup/list/<int:cls>
   * #### 权限: Any
   * @param cls
   */
  listSignup(cls: number): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", `/signup/list/${cls}`);
  }
  /**
   * ## 审核一个报名
   * ### [POST] /signup/<int:volId>/<int:stuId>/audit
   * #### 权限: Class | Teacher
   * @param volId
   * @param stuId
   */
  auditSignup(volId: number,
    stuId: number): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", `/signup/${volId}/${stuId}/audit`);
  }
  /**
   * ## 报名一个义工
   * ### [POST] /signup/<int:volId>
   * #### 权限: Any
   * @param students
   * @param volId
   */
  signup(
    volId: number,
    students: Array<number>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/signup/${volId}`,
      students);
  }
  /**
   * ## 撤回一个报名
   * ### [POST] /signup/<int:volId>/<int:stuId>/rollback
   * #### 权限: Any
   * @param volId
   * @param stuId
   */
  rollback(volId: number,
    stuId: number): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", `/signup/${volId}/${stuId}/rollback`);
  }
  /**
   * ## 搜索感想
   * ### [GET] /thought/search
   * #### 权限: Any
   * @param cls
   * @param status
   * @param student
   * @param Volunteer
   */
  searchThoughts(
    cls?: number,
    status?: enums.ThoughtStatus,
    student?: number,
    Volunteer?: number
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "GET",
      `/thought/search`,
      ...Array<any>(
        cls,
        status,
        student,
        Volunteer
      ).filter((value: any) => value != undefined));
  }
  /**
   * ## 获取一个感想的详细信息
   * ### [GET] /thought/<int:volId>/<int:stuId>
   * #### 权限: Any
   * @param volId
   * @param stuId
   */
  getThoughtInfo(volId: number,
    stuId: number): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", `/thought/${volId}/${stuId}`);
  }
  /**
   * ## 保存感想草稿
   * ### [POST] /thought/<int:volId>/<int:stuId>/save
   * #### 权限: Any
   * @param thought
   * @param pictures
   * @param volId
   * @param stuId
   */
  saveThought(
    volId: number,
    stuId: number,
    thought: string,
    pictures: Array<string>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/thought/${volId}/${stuId}/save`,
      thought,
      pictures);
  }
  /**
   * ## 提交感想
   * ### [POST] /thought/<int:volId>/<int:stuId>/submit
   * #### 权限: Any
   * @param thought
   * @param pictures
   * @param volId
   * @param stuId
   */
  submitThought(
    volId: number,
    stuId: number,
    thought: string,
    pictures: Array<string>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/thought/${volId}/${stuId}/submit`,
      thought,
      pictures);
  }
  /**
   * ## 初审感想(班内)
   * ### [POST] /thought/<int:volId>/<int:stuId>/audit/first
   * #### 权限: Class | Teacher
   * @param volId
   * @param stuId
   */
  firstAudit(volId: number,
    stuId: number): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", `/thought/${volId}/${stuId}/audit/first`);
  }
  /**
   * ## 终审感想(义管会)
   * ### [POST] /thought/<int:volId>/<int:stuId>/audit/final
   * #### 权限: Auditor
   * @param volId
   * @param stuId
   */
  finalAudit(volId: number,
    stuId: number): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", `/thought/${volId}/${stuId}/audit/final`);
  }
  /**
   * ## 打回感想
   * ### [POST] /thought/<int:volId>/<int:stuId>/repulse
   * #### 权限: Any
   * @param reason
   * @param volId
   * @param stuId
   */
  repulse(
    volId: number,
    stuId: number,
    reason: string
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/thought/${volId}/${stuId}/repulse`,
      reason);
  }
  /**
   * ## 检查登录状态
   * ### [GET] /user/check
   * #### 权限: Any
   */
  check(): ForegroundApiRunner<[]> {
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
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/user/login`,
      id,
      pwd);
  }
  /**
   * ## 登出
   * ### [POST] /user/logout
   * #### 权限: Any
   */
  logout(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", `/user/logout`);
  }
  /**
   * ## 搜索用户
   * ### [GET] /user/search
   * #### 权限: Any
   * @param name
   * @param cls
   * @param auth
   */
  searchUsers(
    name?: string,
    cls?: number,
    auth?: number
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "GET",
      `/user/search`,
      ...Array<any>(
        name,
        cls,
        auth
      ).filter((value: any) => value != undefined));
  }
  /**
   * ## 获取一个用户的详细详细信息
   * ### [GET] /user/<int:id>
   * #### 权限: Any
   * @param id
   */
  getUserInfo(id: number): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", `/user/${id}`);
  }
  /**
   * ## 获取一个用户(学生)的义工分
   * ### [GET] /user/<int:id>/time
   * #### 权限: Any
   * @param id
   */
  getVolunteerTime(id: number): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", `/user/${id}/time`);
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
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/user/mod-pwd`,
      old,
      neo);
  }
  /**
   * ## 修改自己(老师)的班级
   * ### [POST] /user/change-class
   * #### 权限: Any
   * @param cls
   */
  changeClass(
    cls: number
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/user/change-class`,
      cls);
  }
  /**
   * ## 创建用户
   * ### [POST] /user/create
   * #### 权限: System
   * @param users
   */
  createUser(
    users: Array<structs.OneUser>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/user/create`,
      users);
  }
  /**
   * ## 修改用户信息
   * ### [POST] /user/<int:id>/modify
   * #### 权限: System
   * @param name
   * @param cls
   * @param auth
   * @param id
   */
  modifyUser(
    id: number,
    name: string,
    cls: number,
    auth: number
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/user/${id}/modify`,
      name,
      cls,
      auth);
  }
  /**
   * ## 删除用户
   * ### [POST] /user/<int:id>/delete
   * #### 权限: System
   * @param id
   */
  deleteUser(id: number): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", `/user/${id}/delete`);
  }
  /**
   * ## 搜索义工
   * ### [GET] /volunteer/search
   * #### 权限: Any
   * @param holder
   * @param student
   * @param cls
   * @param name
   * @param status
   */
  searchVolunteers(
    holder?: number,
    student?: number,
    cls?: number,
    name?: string,
    status?: enums.VolStatus
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "GET",
      `/volunteer/search`,
      ...Array<any>(
        holder,
        student,
        cls,
        name,
        status
      ).filter((value: any) => value != undefined));
  }
  /**
   * ## 获取一个义工的详细信息
   * ### [GET] /volunteer/<int:id>
   * #### 权限: Any
   * @param id
   */
  getVolunteerInfo(id: number): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", `/volunteer/${id}`);
  }
  /**
   * ## 创建一个义工
   * ### [POST] /volunteer/create
   * #### 权限: Any
   * @param name
   * @param description
   * @param time
   * @param type
   * @param reward
   * @param classes
   */
  createVolunteer(
    name: string,
    description: string,
    time: string,
    type: enums.VolType,
    reward: number,
    classes: Array<structs.ClassVol>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/volunteer/create`,
      name,
      description,
      time,
      type,
      reward,
      classes);
  }
  /**
   * ## 修改义工
   * ### [POST] /volunteer/<int:id>/modify
   * #### 权限: Any
   * @param name
   * @param description
   * @param time
   * @param type
   * @param reward
   * @param classes
   * @param id
   */
  modifyVolunteer(
    id: number,
    name: string,
    description: string,
    time: string,
    type: enums.VolType,
    reward: number,
    classes: Array<structs.ClassVol>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      `/volunteer/${id}/modify`,
      name,
      description,
      time,
      type,
      reward,
      classes);
  }
  /**
   * ## 删除义工
   * ### [POST] /volunteer/<int:id>/delete
   * #### 权限: Any
   * @param id
   */
  deleteVolunteer(id: number): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", `/volunteer/${id}/delete`);
  }
  /**
   * ## 审核义工(班内)
   * ### [POST] /volunteer/<int:id>/audit
   * #### 权限: Class | Teacher
   * @param id
   */
  auditVolunteer(id: number): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", `/volunteer/${id}/audit`);
  }

  //--METHODS END----

}

export const fApi = new ForegroundApi({
  beforeRequest(info: ReqInfo) { },
  afterRequest(info: ReqInfo) { },
  errorRequest(e: Error, info: ReqInfo) { },

  notSuccessed(res: AxiosResponse<any>, info: ReqInfo) { },
  successed(res: AxiosResponse<any>, info: ReqInfo) { },

  beforeProcess(info: ReqInfo) { },
  afterProcess(info: ReqInfo) { },
  errorProcess(e: Error, info: ReqInfo) { },

  cleanup(info: ReqInfo) { },
});
