import { useInfoStore, useLoadingStore, useDialogStore } from "@/stores";
import { type AxiosResponse } from "axios";
import axios, { currentToken, setCurrentToken } from "@/plugins/axios";
import * as structs from "./types/structs";
import * as enums from "./types/enums";
import { toasts } from "@/plugins/toastification";

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
  beforeReq(info: ReqInfo, ctx: ReqCtx): void;
  errorReq(e: Error, info: ReqInfo, ctx: ReqCtx): void;

  successedRes(res: AxiosResponse<any>, info: ReqInfo, ctx: ReqCtx): void;
  failedRes(res: AxiosResponse<any> | undefined, info: ReqInfo, ctx: ReqCtx): void;

  afterProcess(info: ReqInfo, ctx: ReqCtx): void;
  errorProcess(e: Error, info: ReqInfo, ctx: ReqCtx): void;

  cleanup(info: ReqInfo, ctx: ReqCtx): void;

  defaultFailedToast: boolean;
  defaultOkToast: boolean;
}

interface ReqInfo {
  url: string;
  method: MethodType;
  id: number;
}

export type ReqCtx = Record<string | number | symbol, unknown>;

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

  const ctx = {};

  const methods = {
    POST: axios.post,
    GET: axios.get,
    DELETE: axios.delete,
    PUT: axios.put,
    PATCH: axios.patch,
  } as const;

  const func = methods[method];
  if (!func) {
    config.errorReq(new Error(`Method ${method} is not supported`), info, ctx);
  }

  return async (processor: ForegroundApiProcessor<R> = () => {}) => {
    config.beforeReq(info, ctx);
    try {
      let res;
      try {
        if(currentToken===""){
          setCurrentToken(useInfoStore().token)
        }
        res = await func(url, ...args); //axios
      } catch (e: any) {
        if (config.defaultFailedToast) {
          if (e?.code === "ERR_NETWORK") {
            toasts.error("网络异常！请链接校内网络。");
          } else {
            toasts.error((e as Error).message);
          }
        }
        config.errorReq(e as Error, info, ctx);
        throw e;
      }

      if (res?.data?.type !== "SUCCESS") {
        config.failedRes(res, info, ctx);
        if (config.defaultFailedToast) {
          toasts.error(res?.data?.message);
        }
      } else {
        const { message, result } = res?.data;
        config.successedRes(res, info, ctx);
        try {
          await processor(result);
          if (config.defaultOkToast) {
            toasts.success(message);
          }
          config.afterProcess(info, ctx);
        } catch (e) {
          config.errorProcess(e as Error, info, ctx);
        }
        config.afterProcess(info, ctx);
      }
    } finally {
      config.cleanup(info, ctx);
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

  get skipFailedToast(): ForegroundApi {
    return new ForegroundApi({
      ...this.config,
      defaultFailedToast: false,
    });
  }

  get loadingState(): ForegroundApi {
    const loadingSymbolKey = Symbol();
    const oldConfig: ForegroundApiConfig = this.config;
    return new ForegroundApi({
      ...oldConfig,
      beforeReq(info, ctx) {
        oldConfig.beforeReq(info, ctx);
        ctx[loadingSymbolKey] = useLoadingStore().incLoading();
      },
      cleanup(info, ctx) {
        oldConfig.cleanup(info, ctx);
        useLoadingStore().decLoading(ctx[loadingSymbolKey] as symbol);
      },
    });
  }

  setFailedRes(onFailedRes:(res: AxiosResponse<any> | undefined, info: ReqInfo)=>void){
    return new ForegroundApi({
      ...this.config,
      failedRes:onFailedRes
    });
  }

  //--METHODS START----
  //${METHODS}
  //--METHODS END----
}

export const fApiNotLoading = new ForegroundApi({
  beforeReq(info: ReqInfo, ctx: ReqCtx) {},
  errorReq(e: Error, info: ReqInfo, ctx: ReqCtx) {},

  successedRes(res: AxiosResponse<any>, info: ReqInfo, ctx: ReqCtx) {},
  failedRes(res: AxiosResponse<any> | undefined, info: ReqInfo, ctx: ReqCtx) {},

  afterProcess(info: ReqInfo, ctx: ReqCtx) {},
  errorProcess(e: Error, info: ReqInfo, ctx: ReqCtx) {},

  cleanup(info: ReqInfo, ctx: ReqCtx) {},

  defaultFailedToast: true,
  defaultOkToast: true,
});

export const fApi = fApiNotLoading.loadingState;
