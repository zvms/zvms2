import { fApi as realFApi } from "./fApi";
import { checkToken as realCheckToken } from "./checkToken";
import { initAxios as realInitAxios } from "./initAxios";
import { logout as realLogout } from "./logout";

import { fApi as mockFApi } from "./mockApis/fApi";
import { checkToken as mockCheckToken } from "./mockApis/checkToken";
import { initAxios as mockInitAxios } from "./mockApis/initAxios";
import { logout as mockLogout } from "./mockApis/logout";

import { devConfig } from "../dev";

export const initAxios = devConfig.backend === "mock" ? mockInitAxios : realInitAxios;
export const fApi = devConfig.backend === "mock" ? mockFApi : realFApi;
export const checkToken = devConfig.backend === "mock" ? mockCheckToken : realCheckToken;
export const logout = devConfig.backend === "mock" ? mockLogout : realLogout;