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
  //${METHODS}
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
