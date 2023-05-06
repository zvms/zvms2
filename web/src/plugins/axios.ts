import Axios from "axios";

export const serverIP = "172.16.5.4";
export const baseURL = `https://kermanx-scaling-lamp-q4w4r75jgjgc6wxw-11451.preview.app.github.dev/`;

const axios = Axios.create({
  baseURL,
  withCredentials: true,
  headers: {
    "Content-type": "application/json",
  },
  timeout: 10000,
  timeoutErrorMessage:"服务器连接超时，请检查网络状态，也有可能是正在维护服务器。",
});

let currentToken: string = "";
export function setCurrentToken(token: string){
  currentToken = token;
}
export {currentToken}

axios.interceptors.request.use(
  (config) => {
    config.params = {
      ...config.params,
    };
    config.headers = config.headers ?? {};
    config.headers.Authorization = currentToken || "";
    return config;
  },
  (error) => Promise.reject(error)
);

export default axios;
