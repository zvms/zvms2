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
   * ### [GET] /class/list
   * #### Authorization: Any
   */
  listClasses(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", "/class/list");
  }
/**
   * ### [GET] /class/<int:id>
   * #### Authorization: Any
   */
  getClassInfo(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", "/class/<int:id>");
  }
/**
   * ### [POST] /class/<int:id>/delete
   * #### Authorization: System
   */
  deleteClass(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", "/class/<int:id>/delete");
  }
/**
   * ### [POST] /class/create
   * #### Authorization: System
   * @param name
   */
  createClass(name: string
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "POST",
        "/class/create",
        name
    );
  }
/**
   * ### [POST] /class/<int:id>/modify
   * #### Authorization: System
   * @param name
   */
  modifyClass(name: string
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "POST",
        "/class/<int:id>/modify",
        name
    );
  }
/**
   * ### [GET] /notice/search
   * #### Authorization: Any
   * @param sender
   * @param user
   * @param cls
   * @param school
   */
  searchNotices(sender?: number,
    user?: number,
    cls?: number,
    school?: any
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "GET",
        "/notice/search",
        ...Array<any>(sender,
        user,
        cls,
        school).filter((value: any) => value != undefined)
    );
  }
/**
   * ### [POST] /notice/send/user
   * #### Authorization: Manager | Teacher
   * @param title
   * @param content
   * @param deadtime
   * @param targets
   */
  sendUserNotice(title: string,
    content: string,
    deadtime: string,
    targets: Array<number>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "POST",
        "/notice/send/user",
        title,
        content,
        deadtime,
        targets
    );
  }
/**
   * ### [POST] /notice/send/class
   * #### Authorization: Manager | Teacher
   * @param title
   * @param content
   * @param deadtime
   * @param targets
   */
  sendClassNotice(title: string,
    content: string,
    deadtime: string,
    targets: Array<number>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "POST",
        "/notice/send/class",
        title,
        content,
        deadtime,
        targets
    );
  }
/**
   * ## [POST] /notice/send/school
   * ### [POST] /notice/send/school
   * #### Authorization: Manager | Teacher
   * @param title
   * @param content
   * @param deadtime
   */
  sendSchoolNotice(title: string,
    content: string,
    deadtime: string
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "POST",
        "/notice/send/school",
        title,
        content,
        deadtime
    );
  }
/**
   * ### [POST] /notice/<int:id>/delete
   * #### Authorization: Manager | Teacher
   */
  deleteNotice(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", "/notice/<int:id>/delete");
  }
/**
   * ### [POST] /notice/<int:id>/modify
   * #### Authorization: Manager | Teacher
   * @param title
   * @param content
   * @param deadtime
   */
  modifyNotice(title: string,
    content: string,
    deadtime: string
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "POST",
        "/notice/<int:id>/modify",
        title,
        content,
        deadtime
    );
  }
/**
   * ### [POST] /report
   * #### Authorization: Any
   * @param report
   */
  report(report: string
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "POST",
        "/report",
        report
    );
  }
/**
   * ### [GET] /signup/list/<int:cls>
   * #### Authorization: Any
   */
  listSignup(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", "/signup/list/<int:cls>");
  }
/**
   * ### [POST] /signup/<int:volId>/<int:stuId>/audit
   * #### Authorization: Class | Teacher
   */
  auditSignup(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", "/signup/<int:volId>/<int:stuId>/audit");
  }
/**
   * ### [POST] /signup/<int:volId>
   * #### Authorization: Any
   * @param students
   */
  signup(students: Array<number>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "POST",
        "/signup/<int:volId>",
        students
    );
  }
/**
   * ## [POST] /signup/<int:volId>/<int:stuId>/audit
   * ### [POST] /signup/<int:volId>/<int:stuId>/rollback
   * #### Authorization: Any
   */
  rollback(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", "/signup/<int:volId>/<int:stuId>/rollback");
  }
/**
   * ### [GET] /thought/search
   * #### Authorization: Any
   * @param cls
   * @param status
   * @param student
   * @param Volunteer
   */
  searchThoughts(cls?: number,
    status?: enums.ThoughtStatus,
    student?: number,
    Volunteer?: number
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "GET",
        "/thought/search",
        ...Array<any>(cls,
        status,
        student,
        Volunteer).filter((value: any) => value != undefined)
    );
  }
/**
   * ### [GET] /thought/<int:volId>/<int:stuId>
   * #### Authorization: Any
   */
  getThoughtInfo(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", "/thought/<int:volId>/<int:stuId>");
  }
/**
   * ## [POST] /thought/<int:volId>/<int:stuId>/save
   * ### [POST] /thought/<int:volId>/<int:stuId>/save
   * #### Authorization: Any
   * @param thought
   * @param pictures
   */
  saveThought(thought: string,
    pictures: Array<string>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "POST",
        "/thought/<int:volId>/<int:stuId>/save",
        thought,
        pictures
    );
  }
/**
   * ### [POST] /thought/<int:volId>/<int:stuId>/submit
   * #### Authorization: Any
   * @param thought
   * @param pictures
   */
  submitThought(thought: string,
    pictures: Array<string>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "POST",
        "/thought/<int:volId>/<int:stuId>/submit",
        thought,
        pictures
    );
  }
/**
   * ### [POST] /thought/<int:volId>/<int:stuId>/audit/first
   * #### Authorization: Class | Teacher
   */
  firstAudit(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", "/thought/<int:volId>/<int:stuId>/audit/first");
  }
/**
   * ### [POST] /thought/<int:volId>/<int:stuId>/audit/final
   * #### Authorization: Auditor
   */
  finalAudit(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", "/thought/<int:volId>/<int:stuId>/audit/final");
  }
/**
   * ## [POST] /thought/<int:volId>/<int:stuId>/audit/repulse
   * ### [POST] /thought/<int:volId>/<int:stuId>/repulse
   * #### Authorization: Any
   * @param reason
   */
  repulse(reason: string
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "POST",
        "/thought/<int:volId>/<int:stuId>/repulse",
        reason
    );
  }
/**
   * ### [GET] /user/check
   * #### Authorization: Any
   */
  check(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", "/user/check");
  }
/**
   * ### [POST] /user/login
   * #### Authorization: Any
   * @param id
   * @param pwd
   */
  login(id: number,
    pwd: string
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "POST",
        "/user/login",
        id,
        pwd
    );
  }
/**
   * ### [POST] /user/logout
   * #### Authorization: Any
   */
  logout(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", "/user/logout");
  }
/**
   * ### [GET] /user/search
   * #### Authorization: Any
   * @param name
   * @param cls
   */
  searchUsers(name?: string,
    cls?: number
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "GET",
        "/user/search",
        ...Array<any>(name,
        cls).filter((value: any) => value != undefined)
    );
  }
/**
   * ### [GET] /user/<int:id>
   * #### Authorization: Any
   */
  getUserInfo(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", "/user/<int:id>");
  }
/**
   * ### [POST] /user/mod-pwd
   * #### Authorization: Any
   * @param old
   * @param neo
   */
  modifyPassword(old: string,
    neo: string
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "POST",
        "/user/mod-pwd",
        old,
        neo
    );
  }
/**
   * ### [POST] /user/change-class
   * #### Authorization: Any
   * @param cls
   */
  changeClass(cls: number
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "POST",
        "/user/change-class",
        cls
    );
  }
/**
   * ### [POST] /user/create
   * #### Authorization: System
   * @param users
   */
  createUser(users: Array<structs.OneUser>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "POST",
        "/user/create",
        users
    );
  }
/**
   * ### [POST] /user/<int:id>/modify
   * #### Authorization: System
   * @param name
   * @param cls
   * @param auth
   */
  modifyUser(name: string,
    cls: number,
    auth: number
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "POST",
        "/user/<int:id>/modify",
        name,
        cls,
        auth
    );
  }
/**
   * ### [POST] /user/<int:id>/delete
   * #### Authorization: System
   */
  deleteUser(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", "/user/<int:id>/delete");
  }
/**
   * ### [GET] /volunteer/search
   * #### Authorization: Any
   * @param holder
   * @param student
   * @param cls
   * @param name
   * @param status
   */
  searchVolunteers(holder?: number,
    student?: number,
    cls?: number,
    name?: string,
    status?: enums.VolStatus
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "GET",
        "/volunteer/search",
        ...Array<any>(holder,
        student,
        cls,
        name,
        status).filter((value: any) => value != undefined)
    );
  }
/**
   * ### [GET] /volunteer/<int:id>
   * #### Authorization: Any
   */
  getVolunteerInfo(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", "/volunteer/<int:id>");
  }
/**
   * ### [POST] /volunteer/create
   * #### Authorization: Any
   * @param name
   * @param description
   * @param time
   * @param type
   * @param reward
   * @param classes
   */
  createVolunteer(name: string,
    description: string,
    time: string,
    type: enums.VolType,
    reward: number,
    classes: Array<structs.ClassVol>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "POST",
        "/volunteer/create",
        name,
        description,
        time,
        type,
        reward,
        classes
    );
  }
/**
   * ### [POST] /volunteer/<int:id>/modify
   * #### Authorization: Any
   * @param name
   * @param description
   * @param time
   * @param type
   * @param reward
   * @param classes
   */
  modifyVolunteer(name: string,
    description: string,
    time: string,
    type: enums.VolType,
    reward: number,
    classes: Array<structs.ClassVol>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
        this,
        "POST",
        "/volunteer/<int:id>/modify",
        name,
        description,
        time,
        type,
        reward,
        classes
    );
  }
/**
   * ### [POST] /volunteer/<int:id>/delete
   * #### Authorization: Any
   */
  deleteVolunteer(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", "/volunteer/<int:id>/delete");
  }
/**
   * ### [POST] /volunteer/<int:id>/audit
   * #### Authorization: Class | Teacher
   */
  auditVolunteer(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", "/volunteer/<int:id>/audit");
  }
  //--METHODS END----
}

export const fApi = new ForegroundApi({
  beforeRequest(info: ReqInfo) {},
  afterRequest(info: ReqInfo) {},
  errorRequest(e: Error, info: ReqInfo) {},

  notSuccessed(res: AxiosResponse<any>, info: ReqInfo) {},
  successed(res: AxiosResponse<any>, info: ReqInfo) {},

  beforeProcess(info: ReqInfo) {},
  afterProcess(info: ReqInfo) {},
  errorProcess(e: Error, info: ReqInfo) {},

  cleanup(info: ReqInfo) {},
});
