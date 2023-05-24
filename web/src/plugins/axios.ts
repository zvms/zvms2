import Axios from "axios";

export const serverIP = "172.31.2.4";
export const baseURL = `http://${serverIP}:11452`;

const axios = Axios.create({
  baseURL,
  withCredentials: true,
  headers: {
    "Content-type": "application/json",
  },
  timeout: 10000,
  timeoutErrorMessage:
    "服务器连接超时，请检查网络状态，也有可能是正在维护服务器。",
});

let currentToken: string = "";
export function setCurrentToken(token: string) {
  currentToken = token;
}
export { currentToken };

axios.interceptors.request.use(
  (config) => {
    config.params = {
      ...config.params,
    };
    config.headers = config.headers ?? {};
    config.headers.Authorization = currentToken ?? "";
    return config;
  },
  (error) => Promise.reject(error)
);

export default axios;
