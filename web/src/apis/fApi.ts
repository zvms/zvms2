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
   * ## [GET] /classes
   */
  listClasses(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", "/classes");
  }

  /**
   * ## [POST] /classes * @param name
   */
  createClass(name: string): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", "/classes", name);
  }
  /**
   * ## [GET] /classes/<int:id>
   */
  getClassInfo(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", "/classes/<int:id>");
  }

  /**
   * ## [DELETE] /classes/<int:id>
   */
  deleteClass(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "DELETE", "/classes/<int:id>");
  }

  /**
   * ## [PUT] /classes/<int:id>
   */
  modifyClass(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "PUT", "/classes/<int:id>");
  }
  /**
   * ## [GET] /notices
   */
  searchNotices(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", "/notices");
  }

  /**
   * ## [POST] /notices * @param title
   * @param content
   * @param deadtime
   * @param type
   * @param targets
   */
  sendNotice(
    title: string,
    content: string,
    deadtime: string,
    type: number,
    targets: Array<number>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      "/notices",
      title,
      content,
      deadtime,
      type,
      targets
    );
  }
  /**
   * ## [GET] /notices/<int:id>
   */
  getNotice(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", "/notices/<int:id>");
  }

  /**
   * ## [DELETE] /notices/<int:id>
   */
  deleteNotice(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "DELETE", "/notices/<int:id>");
  }

  /**
   * ## [PUT] /notices/<int:id>
   */
  updateNotice(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "PUT", "/notices/<int:id>");
  }
  /**
   * ## [POST] /report * @param content
   */
  report(content: string): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", "/report", content);
  }
  /**
   * ## [GET] /signup
   */
  listSignup(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", "/signup");
  }
  /**
   * ## [POST] /signup/<int:stuId> * @param volId
   */
  signup(volId: number): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      "/signup/<int:stuId>",
      volId
    );
  }
  /**
   * ## [PATCH] /signup/<int:stuId>/<int:volId>
   */
  auditSignup(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "PATCH",
      "/signup/<int:stuId>/<int:volId>"
    );
  }

  /**
   * ## [DELETE] /signup/<int:stuId>/<int:volId>
   */
  rollback(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "DELETE",
      "/signup/<int:stuId>/<int:volId>"
    );
  }
  /**
   * ## [GET] /thoughts
   */
  searchThoughts(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", "/thoughts");
  }
  /**
   * ## [GET] /thoughts/<int:stuId> * @param volid
   */
  signup(volid: number): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "GET",
      "/thoughts/<int:stuId>",
      volid
    );
  }
  /**
   * ## [GET] /thoughts/<int:stuId>/<int:volId>
   */
  getThoughtInfo(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "GET",
      "/thoughts/<int:stuId>/<int:volId>"
    );
  }

  /**
   * ## [PATCH] /thoughts/<int:stuId>/<int:volId>
   */
  updateThought(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "PATCH",
      "/thoughts/<int:stuId>/<int:volId>"
    );
  }
  /**
   * ## [GET] /users
   */
  searchUsers(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", "/users");
  }
  /**
   * ## [GET] /users/check
   */
  check(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", "/users/check");
  }

  /**
   * ## [POST] /users/login * @param id
   * @param pwd
   */
  login(id: number, pwd: string): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", "/users/login", id, pwd);
  }

  /**
   * ## [POST] /users/logout
   */
  logout(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", "/users/logout");
  }

  /**
   * ## [POST] /users/create * @param users
   */
  createUsers(users: Array<structs.UserOfUsers>): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "POST", "/users/create", users);
  }

  /**
   * ## [PATCH] /users/mod-pwd * @param oldMD5
   * @param newMD5
   */
  modifyPassword(oldMD5: string, newMD5: string): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "PATCH",
      "/users/mod-pwd",
      oldMD5,
      newMD5
    );
  }

  /**
   * ## [PATCH] /users/change-class * @param newClsId
   */
  changeClass(newClsId: number): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "PATCH",
      "/users/change-class",
      newClsId
    );
  }

  /**
   * ## [GET] /users/<int:id>
   */
  getUserInfo(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", "/users/<int:id>");
  }

  /**
   * ## [DELETE] /users/<int:id>
   */
  deleteUser(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "DELETE", "/users/<int:id>");
  }

  /**
   * ## [PUT] /users/<int:id>
   */
  modifyUser(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "PUT", "/users/<int:id>");
  }
  /**
   * ## [GET] /volunteers
   */
  searchVolunteers(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", "/volunteers");
  }

  /**
   * ## [POST] /volunteers * @param name
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
    type: number,
    reward: number,
    classes: Array<structs.VolunteerRecordClass>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "POST",
      "/volunteers",
      name,
      description,
      time,
      type,
      reward,
      classes
    );
  }
  /**
   * ## [GET] /volunteers/<int:id>
   */
  getVolunteerInfo(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "GET", "/volunteers/<int:id>");
  }

  /**
   * ## [PUT] /volunteers/<int:id> * @param name
   * @param description
   * @param time
   * @param type
   * @param reward
   * @param classes
   */
  updateVolunteer(
    name: string,
    description: string,
    time: string,
    type: number,
    reward: number,
    classes: Array<structs.VolunteerRecordClass>
  ): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(
      this,
      "PUT",
      "/volunteers/<int:id>",
      name,
      description,
      time,
      type,
      reward,
      classes
    );
  }

  /**
   * ## [DELETE] /volunteers/<int:id>
   */
  deleteVolunteer(): ForegroundApiRunner<[]> {
    return createForegroundApiRunner(this, "DELETE", "/volunteers/<int:id>");
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
