import { useInfoStore } from "@/stores";
import Axios from "axios";

export const baseURL = "http://172.28.1.13:1145";//"http://172.31.2.3:1145";

const axios = Axios.create({
  baseURL,
  withCredentials: true,
  headers: {
    "Content-type": "application/json",
  },
  timeout: 6000,
});

axios.interceptors.request.use(
  (config) => {
    const infoStore = useInfoStore();
    config.params = {
      ...config.params,
    };
    config.headers = config.headers ?? {};
    config.headers.Authorization = infoStore.token || "";
    return config;
  },
  (error) => Promise.reject(error)
);

export default axios;
