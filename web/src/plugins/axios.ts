import { useInfoStore } from "@/stores";
import Axios from "axios";

export const serverIP = "172.31.2.4";
export const baseURL = `http://${serverIP}:1145`;

const axios = Axios.create({
  baseURL,
  withCredentials: true,
  headers: {
    "Content-type": "application/json",
  },
  timeout: 10000,
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
